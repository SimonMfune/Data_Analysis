"""Milestone M3: configurable cleaning that records every change it makes."""
from dataclasses import dataclass

import pandas as pd

PLACEHOLDERS = ["N/A", "NA", "n/a", "null", "NULL", "-", "?"]


@dataclass(frozen=True)          # frozen, so options can be a cache key
class CleaningOptions:
    strip_text: bool = True
    placeholders_missing: bool = False
    drop_duplicates: bool = True
    drop_empty_columns: bool = True
    numeric_missing: str = "leave"     # "leave", "median" or "drop rows"
    text_missing: str = "leave"        # "leave" or "fill Unknown"


def _text_columns(df):
    return [c for c in df.columns
            if pd.api.types.is_string_dtype(df[c]) or isinstance(df[c].dtype, pd.CategoricalDtype)]


def clean(df: pd.DataFrame, options: CleaningOptions) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply the chosen steps in a fixed order. Returns the cleaned data and a change log
    with one row per step that changed something."""
    # TODO M3: write this function
    raise NotImplementedError("M3: clean")
