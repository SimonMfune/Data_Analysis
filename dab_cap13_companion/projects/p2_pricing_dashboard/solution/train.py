"""Milestone M1: train, evaluate and save the pricing model. Run from this folder: python train.py"""
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict, train_test_split

from features import FEATURES, TARGET, build_model

HERE = Path(__file__).parent
DATA = HERE.parents[2] / "data" / "clean" / "kb_product_pricing.csv"
SEED, COVERAGE = 2026, 0.80


def main():
    products = pd.read_csv(DATA)
    X, y = products[FEATURES], products[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

    # Interval: quantiles of out-of-fold log residuals on the training set
    folds = KFold(5, shuffle=True, random_state=SEED)
    oof = cross_val_predict(build_model(), X_train, y_train, cv=folds)
    log_resid = np.log(y_train) - np.log(oof)
    q_low, q_high = np.quantile(log_resid, [(1 - COVERAGE) / 2, 1 - (1 - COVERAGE) / 2])

    model = build_model().fit(X_train, y_train)
    pred = model.predict(X_test)
    inside = ((y_test >= pred * np.exp(q_low)) & (y_test <= pred * np.exp(q_high))).mean()
    metrics = {"test_MAPE": mean_absolute_percentage_error(y_test, pred),
               "test_MAE": mean_absolute_error(y_test, pred), "test_R2": r2_score(y_test, pred),
               "cv_MAPE": float(np.mean(np.abs(oof - y_train) / y_train)),
               "interval_coverage_test": float(inside)}

    reg = model.regressor_.named_steps["regress"]
    names = [n.split("__")[1] for n in model.regressor_.named_steps["prepare"].get_feature_names_out()]
    effects = pd.Series(reg.coef_, index=names)

    final = build_model().fit(X, y)                 # refit on all products for serving
    artefact = {
        "model": final, "interval_log_quantiles": (float(q_low), float(q_high)), "coverage": COVERAGE,
        "metrics": metrics, "effects": effects,
        "test_predictions": pd.DataFrame({"actual": y_test, "predicted": pred}),
        "training_rows": len(products), "cost_range": (float(X["unit_cost_zmw"].min()),
                                                        float(X["unit_cost_zmw"].max())),
        "trained_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "versions": {"scikit-learn": sklearn.__version__, "pandas": pd.__version__, "numpy": np.__version__},
    }
    out = HERE / "artefacts" / "price_model.joblib"
    out.parent.mkdir(exist_ok=True)
    joblib.dump(artefact, out)

    print(f"Trained on {len(X_train)} products, tested on {len(X_test)}")
    print(f"Test MAPE {metrics['test_MAPE']:.1%}   MAE K{metrics['test_MAE']:.2f}   R² {metrics['test_R2']:.3f}")
    print(f"80% interval: x{np.exp(q_low):.3f} to x{np.exp(q_high):.3f} of the model price")
    print(f"Test prices inside their interval: {inside:.1%}")
    print(f"Saved {out.name} (refitted on all {len(products)} products)")


if __name__ == "__main__":
    main()
