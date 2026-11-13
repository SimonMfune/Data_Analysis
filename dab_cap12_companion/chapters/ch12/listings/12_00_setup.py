import matplotlib
matplotlib.use("Agg")                      # draw to files; in a notebook, omit this line
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

plt.style.use("shared/kb.mplstyle")
pd.set_option("display.width", 88)
FIG = "chapters/ch12/figures/"
SEED = 2026

churn = pd.read_csv("data/clean/kb_customer_churn.csv")
numeric = ["tenure_days", "age", "orders_total", "orders_last_90d", "orders_last_180d",
           "spend_last_180d_zmw", "avg_basket_zmw", "recency_days", "pct_orders_delayed",
           "pct_orders_campaign", "app_share", "returns_count", "avg_rating_given"]
categorical = ["province", "signup_channel", "preferred_payment"]
