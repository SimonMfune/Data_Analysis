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
    # TODO M2: write this function
    raise NotImplementedError("M2: suggest")
