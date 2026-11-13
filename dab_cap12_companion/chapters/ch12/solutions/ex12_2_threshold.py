"""Exercise 12.2 solution: the best threshold for two retention offers."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

churn = pd.read_csv("data/clean/kb_customer_churn.csv")
numeric = ["tenure_days", "age", "orders_total", "orders_last_90d", "orders_last_180d",
           "spend_last_180d_zmw", "avg_basket_zmw", "recency_days", "pct_orders_delayed",
           "pct_orders_campaign", "app_share", "returns_count", "avg_rating_given"]
categorical = ["province", "signup_channel", "preferred_payment"]
X, y = churn[numeric + categorical], churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=2026)
model = Pipeline([("prepare", ColumnTransformer([
    ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("categories", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical)])),
    ("classify", LogisticRegression(max_iter=1000))])
folds = StratifiedKFold(5, shuffle=True, random_state=2026)
oof = cross_val_predict(model, X_train, y_train, cv=folds, method="predict_proba")[:, 1]
test_p = model.fit(X_train, y_train).predict_proba(X_test)[:, 1]
margin = churn.loc[churn["churned"] == 1, "spend_last_180d_zmw"].mean() * 0.365


def benefit(y_true, p, t, cost, save):
    flag = p >= t
    return ((flag & (y_true == 1)).sum() * (save * margin - cost) - (flag & (y_true == 0)).sum() * cost)


ts = np.round(np.arange(0.05, 0.81, 0.01), 2)
for name, cost, save in [("K150 voucher, saves 30%", 150, 0.30), ("K80 fee waiver, saves 20%", 80, 0.20)]:
    curve = [benefit(y_train.to_numpy(), oof, t, cost, save) for t in ts]
    t_best = ts[int(np.argmax(curve))]
    flagged = int((test_p >= t_best).sum())
    print(f"{name:<26} break-even precision {cost / (save * margin):.2f}; chosen threshold {t_best:.2f}; "
          f"test: {flagged} flagged, net benefit K{benefit(y_test.to_numpy(), test_p, t_best, cost, save):,.0f}")
