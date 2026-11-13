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
    out = df.copy()
    log = []

    def record(step, detail, affected):
        if affected:
            log.append({"step": step, "detail": detail, "affected": int(affected)})

    if options.strip_text:
        changed = 0
        for col in _text_columns(out):
            as_text = out[col].astype("string")
            stripped = as_text.str.strip()
            changed += int((as_text != stripped).fillna(False).sum())
            if isinstance(out[col].dtype, pd.CategoricalDtype):
                out[col] = stripped.astype("category")
            else:
                out[col] = stripped
        record("Strip spaces", "Removed leading and trailing spaces from text", changed)

    if options.placeholders_missing:
        before = int(out.isna().sum().sum())
        for col in _text_columns(out):
            out[col] = out[col].mask(out[col].astype("string").isin(PLACEHOLDERS))
        record("Placeholders", f"Treated {', '.join(PLACEHOLDERS)} as missing",
               int(out.isna().sum().sum()) - before)

    if options.drop_empty_columns:
        empty = [c for c in out.columns if out[c].isna().all()]
        out = out.drop(columns=empty)
        record("Empty columns", f"Dropped: {', '.join(empty)}", len(empty))

    if options.drop_duplicates:
        n = len(out)
        out = out.drop_duplicates()
        record("Duplicates", "Dropped exact duplicate rows", n - len(out))

    numbers = out.select_dtypes("number").columns
    if options.numeric_missing == "median":
        for col in numbers:
            gaps = int(out[col].isna().sum())
            if gaps:
                median = out[col].median()
                out[col] = out[col].fillna(median)
                record("Fill numbers", f"{col}: filled with median {median:,.2f}", gaps)
    elif options.numeric_missing == "drop rows":
        n = len(out)
        out = out.dropna(subset=numbers)
        record("Drop rows", "Dropped rows with a missing number", n - len(out))

    if options.text_missing == "fill Unknown":
        for col in _text_columns(out):
            gaps = int(out[col].isna().sum())
            if gaps:
                if isinstance(out[col].dtype, pd.CategoricalDtype):
                    out[col] = out[col].cat.add_categories("Unknown")
                out[col] = out[col].fillna("Unknown")
                record("Fill text", f"{col}: filled with 'Unknown'", gaps)

    return out.reset_index(drop=True), pd.DataFrame(log, columns=["step", "detail", "affected"])
