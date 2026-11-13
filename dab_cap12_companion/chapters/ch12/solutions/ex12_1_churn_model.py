"""Exercise 12.1 solution: a churn model with a confusion matrix and the four metrics."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

churn = pd.read_csv("data/clean/kb_customer_churn.csv")
numeric = ["tenure_days", "age", "orders_total", "orders_last_90d", "orders_last_180d",
           "spend_last_180d_zmw", "avg_basket_zmw", "recency_days", "pct_orders_delayed",
           "pct_orders_campaign", "app_share", "returns_count", "avg_rating_given"]
categorical = ["province", "signup_channel", "preferred_payment"]
X, y = churn[numeric + categorical], churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=2026)

prepare = ColumnTransformer([
    ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
    ("categories", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical)])

for weight in [None, "balanced"]:
    m = Pipeline([("prepare", prepare),
                  ("classify", LogisticRegression(max_iter=1000, class_weight=weight))]).fit(X_train, y_train)
    p = m.predict(X_test)
    print(f"class_weight={weight}")
    print(pd.DataFrame(confusion_matrix(y_test, p), index=["actual stayed", "actual churned"],
                       columns=["predicted stays", "predicted churns"]).to_string())
    print(f"accuracy {accuracy_score(y_test, p):.3f}  precision {precision_score(y_test, p):.3f}  "
          f"recall {recall_score(y_test, p):.3f}  F1 {f1_score(y_test, p):.3f}\n")
