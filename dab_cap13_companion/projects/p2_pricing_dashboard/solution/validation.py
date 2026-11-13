"""Milestone M5: check an uploaded batch before scoring it."""
import pandas as pd

from features import CATEGORIES, FEATURES, TIERS

LIMITS = {"weight_kg": (0.01, 100.0), "unit_cost_zmw": (1.0, 50_000.0)}


def validate_batch(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Return (rows that can be scored, list of problems). A missing column is fatal;
    other problems reject only the rows concerned, each with a row-numbered message."""
    problems = []
    df = df.rename(columns=lambda c: str(c).strip())
    missing = [c for c in FEATURES if c not in df.columns]
    if missing:
        return df.iloc[0:0], [f"Missing column(s): {', '.join(missing)}. "
                              f"Required: {', '.join(FEATURES)}."]
    if df.empty:
        return df, ["The file has a header but no rows."]

    bad = pd.Series(False, index=df.index)
    for col in ["weight_kg", "unit_cost_zmw", "imported_flag"]:
        values = pd.to_numeric(df[col], errors="coerce")
        for i in df.index[values.isna()]:
            problems.append(f"Row {i + 2}: {col} must be a number (got {df.at[i, col]!r})")
        bad |= values.isna()
        df[col] = values
    for col, (lo, hi) in LIMITS.items():
        outside = df[col].notna() & ~df[col].between(lo, hi)
        for i in df.index[outside]:
            problems.append(f"Row {i + 2}: {col} = {df.at[i, col]:g} is outside {lo:g} to {hi:g}")
        bad |= outside
    flag_bad = df["imported_flag"].notna() & ~df["imported_flag"].isin([0, 1])
    for i in df.index[flag_bad]:
        problems.append(f"Row {i + 2}: imported_flag must be 0 or 1")
    bad |= flag_bad
    for col, allowed in [("category", CATEGORIES), ("brand_tier", TIERS)]:
        df[col] = df[col].astype("string").str.strip()
        unknown = ~df[col].isin(allowed)
        for i in df.index[unknown]:
            problems.append(f"Row {i + 2}: {col} {df.at[i, col]!r} is not one of: {', '.join(allowed)}")
        bad |= unknown
    problems.sort(key=lambda m: int(m.split(':')[0].split()[1]))      # in row order
    good = df.loc[~bad].copy()
    good["imported_flag"] = good["imported_flag"].astype(int)
    return good, problems
