"""The model's inputs, their rules, and the pipeline that turns them into a price (Chapter 11)."""
import numpy as np
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

TARGET = "list_price_zmw"
CATEGORICAL = ["category", "brand_tier"]
NUMERIC = ["imported_flag", "weight_kg", "unit_cost_zmw"]
FEATURES = CATEGORICAL + NUMERIC
CATEGORIES = ["Baby & Kids", "Electronics", "Fashion", "Groceries", "Health & Beauty",
              "Home & Kitchen", "Household", "Stationery"]
TIERS = ["Value", "Standard", "Premium"]


def build_model() -> TransformedTargetRegressor:
    """The log-log linear model chosen in Chapter 11: log(price) on log(cost), log(weight),
    category, brand tier and the imported flag."""
    prepare = ColumnTransformer([
        ("categories", OneHotEncoder(drop="first", handle_unknown="ignore"), CATEGORICAL),
        ("logs", FunctionTransformer(np.log, feature_names_out="one-to-one"), ["unit_cost_zmw", "weight_kg"]),
        ("flag", "passthrough", ["imported_flag"]),
    ])
    return TransformedTargetRegressor(
        regressor=Pipeline([("prepare", prepare), ("regress", LinearRegression())]),
        func=np.log, inverse_func=np.exp)
