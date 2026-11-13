"""Exercise 12.3 solution: a fairness audit with bootstrap confidence intervals."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

rng = np.random.default_rng(2026)
churn = pd.read_csv("data/clean/kb_customer_churn.csv")
numeric = ["tenure_days", "age", "orders_total", "orders_last_90d", "orders_last_180d",
           "spend_last_180d_zmw", "avg_basket_zmw", "recency_days", "pct_orders_delayed",
           "pct_orders_campaign", "app_share", "returns_count", "avg_rating_given"]
categorical = ["province", "signup_channel", "preferred_payment"]
model = Pipeline([("prepare", ColumnTransformer([
    ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("categories", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical)])),
    ("classify", LogisticRegression(max_iter=1000))])
folds = StratifiedKFold(5, shuffle=True, random_state=2026)
p = cross_val_predict(model, churn[numeric + categorical], churn["churned"], cv=folds,
                      method="predict_proba")[:, 1]
d = churn[["gender", "province"]].assign(y=churn["churned"].to_numpy(), flag=p >= 0.43)


def ci(values, stat, reps=2000):
    vals = [stat(values.sample(len(values), replace=True, random_state=int(rng.integers(1e9))))
            for _ in range(reps)]
    return np.nanpercentile(vals, [2.5, 97.5])


def recall(g):
    return g.loc[g["y"] == 1, "flag"].mean()


def precision(g):
    return g.loc[g["flag"], "y"].mean() if g["flag"].any() else np.nan


rows = []
for col in ["gender", "province"]:
    for name, g in d.groupby(col):
        r_lo, r_hi = ci(g, recall)
        p_lo, p_hi = ci(g, precision)
        rows.append({"group": f"{col}: {name}", "n": len(g), "churners": int(g["y"].sum()),
                     "recall": recall(g), "recall_95ci": f"{r_lo:.2f}-{r_hi:.2f}",
                     "precision": precision(g), "precision_95ci": f"{p_lo:.2f}-{p_hi:.2f}"})
table = pd.DataFrame(rows)
print(table.round(3).to_string(index=False))
print(f"\nOverall: recall {recall(d):.3f}, precision {precision(d):.3f}")
