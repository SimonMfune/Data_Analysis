"""Page 4: fit linear or logistic regression on any target the user chooses (Chapters 11-12)."""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (confusion_matrix, f1_score, mean_absolute_error, precision_score,
                             r2_score, recall_score, roc_auc_score, root_mean_squared_error)
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 2026
MAX_LEVELS = 20


@dataclass
class ModelResult:
    kind: str                                  # "linear" or "logistic"
    target: str
    features: list
    n_train: int
    n_test: int
    metrics: dict
    coefficients: pd.DataFrame                 # feature, coefficient (and odds_ratio for logistic)
    y_test: np.ndarray
    test_score: np.ndarray                     # predictions (linear) or probabilities (logistic)
    positive_class: object = None
    notes: list = field(default_factory=list)


def suggest_kind(series: pd.Series) -> str:
    """Logistic for a two-valued target, linear for a numeric one."""
    values = series.dropna().unique()
    if len(values) == 2:
        return "logistic"
    if pd.api.types.is_numeric_dtype(series):
        return "linear"
    raise ValueError("Choose a numeric target, or one with exactly two values.")


def usable_features(df: pd.DataFrame, target: str) -> list[str]:
    """Numbers, flags and categories with at most MAX_LEVELS values; never identifiers or dates."""
    out = []
    for col in df.columns:
        if col == target or pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        s = df[col]
        if pd.api.types.is_numeric_dtype(s) or s.nunique() <= MAX_LEVELS:
            if s.nunique() < len(s.dropna()) or pd.api.types.is_numeric_dtype(s):
                out.append(col)
    return out


def default_features(df: pd.DataFrame, target: str, candidates: list[str], k: int = 6) -> list[str]:
    """A sensible starting set: the k numeric candidates most correlated (in absolute value,
    Spearman) with the target. The user can change it; this only avoids a poor first model."""
    y = df[target]
    if not pd.api.types.is_numeric_dtype(y):
        y = (y == sorted(y.dropna().unique(), key=str)[-1]).astype(int)
    numeric = [c for c in candidates if pd.api.types.is_numeric_dtype(df[c])]
    strength = {c: abs(df[c].corr(y, method="spearman")) for c in numeric}
    ranked = sorted((c for c in numeric if pd.notna(strength[c])), key=strength.get, reverse=True)
    return ranked[:k] or candidates[:k]


def build_pipeline(df: pd.DataFrame, features: list[str], kind: str) -> Pipeline:
    numeric = [c for c in features if pd.api.types.is_numeric_dtype(df[c])]
    categorical = [c for c in features if c not in numeric]
    prepare = ColumnTransformer([
        ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("categories", Pipeline([("fill", SimpleImputer(strategy="most_frequent")),
                                 ("encode", OneHotEncoder(drop="first", handle_unknown="ignore"))]), categorical),
    ])
    model = LogisticRegression(max_iter=2000) if kind == "logistic" else LinearRegression()
    return Pipeline([("prepare", prepare), ("model", model)])


def fit(df: pd.DataFrame, target: str, features: list[str], kind: str) -> ModelResult:
    """Split 75/25, fit, cross-validate on the training part, and evaluate once on the test part."""
    if not features:
        raise ValueError("Choose at least one feature.")
    data = df[features + [target]].dropna(subset=[target])
    notes = []
    if len(data) < len(df):
        notes.append(f"{len(df) - len(data):,} rows with a missing target were left out.")
    X, y = data[features].copy(), data[target]
    for col in X.columns:                     # pandas' NA markers confuse scikit-learn: use NaN
        if not pd.api.types.is_numeric_dtype(X[col]):
            X[col] = X[col].astype(object).where(X[col].notna(), np.nan)
        elif X[col].dtype.kind not in "if":
            X[col] = X[col].astype(float)
    positive = None
    if kind == "logistic":
        classes = sorted(y.unique(), key=str)
        positive = classes[-1]
        y = (y == positive).astype(int)
        positive = positive.item() if hasattr(positive, "item") else positive
        notes.append(f"Positive class: {target} = {positive}.")
    stratify = y if kind == "logistic" else None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=SEED,
                                                        stratify=stratify)
    pipe = build_pipeline(data, features, kind)
    folds = (StratifiedKFold if kind == "logistic" else KFold)(5, shuffle=True, random_state=SEED)
    scoring = "roc_auc" if kind == "logistic" else "r2"
    cv = cross_val_score(pipe, X_train, y_train, cv=folds, scoring=scoring)
    pipe.fit(X_train, y_train)

    names = [n.split("__", 1)[1] for n in pipe.named_steps["prepare"].get_feature_names_out()]
    coefs = pipe.named_steps["model"].coef_.ravel()
    table = pd.DataFrame({"feature": names, "coefficient": coefs})
    if kind == "logistic":
        score = pipe.predict_proba(X_test)[:, 1]
        table["odds_ratio"] = np.exp(coefs)
        metrics = {"cv_auc_mean": cv.mean(), "cv_auc_sd": cv.std(), "test_auc": roc_auc_score(y_test, score),
                   "positive_rate": float(y.mean())}
    else:
        score = pipe.predict(X_test)
        metrics = {"cv_r2_mean": cv.mean(), "cv_r2_sd": cv.std(), "test_r2": r2_score(y_test, score),
                   "test_mae": mean_absolute_error(y_test, score),
                   "test_rmse": root_mean_squared_error(y_test, score)}
    table = table.reindex(table["coefficient"].abs().sort_values(ascending=False).index).reset_index(drop=True)
    return ModelResult(kind, target, list(features), len(X_train), len(X_test),
                       {k: float(v) for k, v in metrics.items()}, table, np.asarray(y_test), score, positive, notes)


def threshold_metrics(result: ModelResult, threshold: float) -> dict:
    """Confusion matrix and the four metrics at a chosen threshold (logistic models)."""
    pred = (result.test_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(result.y_test, pred, labels=[0, 1]).ravel()
    return {"threshold": threshold, "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
            "precision": precision_score(result.y_test, pred, zero_division=0),
            "recall": recall_score(result.y_test, pred, zero_division=0),
            "f1": f1_score(result.y_test, pred, zero_division=0),
            "flagged": int(pred.sum())}
