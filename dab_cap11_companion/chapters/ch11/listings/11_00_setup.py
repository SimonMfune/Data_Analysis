import matplotlib
matplotlib.use("Agg")                      # draw to files; in a notebook, omit this line
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import (mean_absolute_error, mean_absolute_percentage_error,
                             r2_score, root_mean_squared_error)
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

plt.style.use("shared/kb.mplstyle")
pd.set_option("display.width", 88)
pd.set_option("display.max_columns", 10)
FIG = "chapters/ch11/figures/"
SEED = 2026
