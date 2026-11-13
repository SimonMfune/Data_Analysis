"""Milestone M2: describe every column, and the dataset as a whole."""
import pandas as pd


def column_role(s: pd.Series) -> str:
    """A plain-English role for a column: identifier, number, date, category or text."""
    if pd.api.types.is_datetime64_any_dtype(s):
        return "date"
    if pd.api.types.is_bool_dtype(s) or isinstance(s.dtype, pd.CategoricalDtype):
        return "category"
    if pd.api.types.is_numeric_dtype(s):
        return "number"
    present = s.dropna()
    if len(present) and present.nunique() == len(present):
        return "identifier"
    return "text"


def profile_columns(df: pd.DataFrame) -> pd.DataFrame:
    """One row per column: role, dtype, missing values, distinct values and an example."""
    rows = []
    n = len(df)
    for col in df.columns:
        s = df[col]
        missing = int(s.isna().sum())
        distinct = int(s.nunique(dropna=True))
        example = s.dropna().iloc[0] if missing < n else ""
        rows.append({"column": col, "role": column_role(s), "dtype": str(s.dtype),
                     "missing": missing, "missing_pct": round(missing / n * 100, 1) if n else 0.0,
                     "distinct": distinct, "example": str(example)[:30]})
    return pd.DataFrame(rows)


def profile_dataset(df: pd.DataFrame) -> dict:
    """Headline figures for the whole table."""
    return {"rows": len(df), "columns": df.shape[1],
            "missing_cells": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_kb": round(float(df.memory_usage(deep=True).sum()) / 1024, 1)}


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """describe() for number columns, plus skewness, one row per column."""
    nums = df.select_dtypes("number")
    if nums.empty:
        return pd.DataFrame()
    table = nums.describe().T
    table["skew"] = nums.skew()
    return table.rename(columns={"50%": "median"})


def top_values(s: pd.Series, n: int = 10) -> pd.DataFrame:
    """The n most common values of a column with counts and percentages."""
    counts = s.value_counts(dropna=False).head(n)
    return pd.DataFrame({"count": counts, "percent": (counts / len(s) * 100).round(1)})
