"""Milestone M2: describe every column, and the dataset as a whole."""
import pandas as pd


def column_role(s: pd.Series) -> str:
    """A plain-English role for a column: identifier, number, date, category or text."""
    # TODO M2: write this function
    raise NotImplementedError("M2: column_role")


def profile_columns(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: role, dtype, missing values, distinct values and an example."""
    # TODO M2: write this function
    raise NotImplementedError("M2: profile_columns")


def profile_dataset(df: pd.DataFrame) -> dict:
    """Headline figures for the whole table."""
    # TODO M2: write this function
    raise NotImplementedError("M2: profile_dataset")


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """describe() for number columns, plus skewness, one row per column."""
    # TODO M2: write this function
    raise NotImplementedError("M2: numeric_summary")


def top_values(s: pd.Series, n: int = 10) -> pd.DataFrame:
    """The n most common values of a column with counts and percentages."""
    counts = s.value_counts(dropna=False).head(n)
    return pd.DataFrame({"count": counts, "percent": (counts / len(s) * 100).round(1)})
