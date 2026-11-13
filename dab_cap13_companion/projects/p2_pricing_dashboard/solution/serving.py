"""Loading the trained artefact and turning model output into suggestions. Nothing here trains."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from features import FEATURES
from guardrails import apply_guardrails

ARTEFACT = Path(__file__).with_name("artefacts") / "price_model.joblib"


def load_artefact(path: Path = ARTEFACT) -> dict:
    """The dictionary saved by train.py: model, interval quantiles, metrics and metadata."""
    if not path.exists():
        raise FileNotFoundError(f"{path.name} not found. Run `python train.py` first.")
    return joblib.load(path)


def suggest(artefact: dict, products: pd.DataFrame) -> pd.DataFrame:
    """Model price, an 80% interval, and the guarded suggestion for each product.
    Expects validated input (see validation.py); fails loudly if a feature column is missing."""
    missing = [c for c in FEATURES if c not in products.columns]
    if missing:
        raise ValueError(f"Missing feature column(s): {', '.join(missing)}")
    model, (q_low, q_high) = artefact["model"], artefact["interval_log_quantiles"]
    point = model.predict(products)
    out = products.copy()
    out["model_price_zmw"] = point.round(2)
    out["low_zmw"] = (point * np.exp(q_low)).round(2)
    out["high_zmw"] = (point * np.exp(q_high)).round(2)
    guarded = [apply_guardrails(p, c) for p, c in zip(point, products["unit_cost_zmw"])]
    out["suggested_price_zmw"] = [g[0] for g in guarded]
    out["margin_pct"] = ((out["suggested_price_zmw"] - out["unit_cost_zmw"])
                         / out["suggested_price_zmw"] * 100).round(1)
    out["notes"] = ["; ".join(g[1]) for g in guarded]
    return out
