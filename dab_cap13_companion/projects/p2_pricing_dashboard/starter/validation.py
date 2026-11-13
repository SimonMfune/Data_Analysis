"""Milestone M5: check an uploaded batch before scoring it."""
import pandas as pd

from features import CATEGORIES, FEATURES, TIERS

LIMITS = {"weight_kg": (0.01, 100.0), "unit_cost_zmw": (1.0, 50_000.0)}


def validate_batch(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Return (rows that can be scored, list of problems). A missing column is fatal;
    other problems reject only the rows concerned, each with a row-numbered message."""
    # TODO M5: write this function
    raise NotImplementedError("M5: validate_batch")
