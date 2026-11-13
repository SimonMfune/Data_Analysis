"""Unit tests for loader, profiling and cleaning. Run from the solution folder: pytest tests"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cleaning  # noqa: E402
import loader  # noqa: E402
import profiling  # noqa: E402

DATA = Path(__file__).resolve().parents[4] / "data"


@pytest.mark.parametrize("name, encoding, sep, shape", [
    ("fintech_loans.csv", "utf-8-sig", ",", (1200, 9)),
    ("clinic_visits.csv", "utf-8-sig", ";", (900, 9)),
    ("marketing_leads.csv", "cp1252", ",", (700, 8)),
])
def test_unseen_files_load(name, encoding, sep, shape):
    r = loader.load_csv((DATA / "unseen" / name).read_bytes())
    assert (r.encoding, r.delimiter, r.data.shape) == (encoding, sep, shape)


def test_accents_survive():
    r = loader.load_csv((DATA / "unseen" / "marketing_leads.csv").read_bytes())
    assert "Résumé Clinic" in set(r.data["campaign"])


def test_day_first_dates_are_not_swapped():
    r = loader.load_csv((DATA / "unseen" / "clinic_visits.csv").read_bytes())
    assert r.data.loc[0, "visit_date"] == pd.Timestamp("2025-07-11")   # 11/07/2025


def test_profile_matches_pandas():
    df = pd.read_csv(DATA / "unseen" / "fintech_loans.csv")
    r = loader.load_csv((DATA / "unseen" / "fintech_loans.csv").read_bytes())
    prof = profiling.profile_columns(r.data).set_index("column")
    assert prof["missing"].to_dict() == df.isna().sum().to_dict()
    assert prof.loc["purpose", "distinct"] == df["purpose"].nunique()
    assert prof.loc["loan_id", "role"] == "identifier"


def test_currency_text_becomes_numbers():
    s = pd.Series(["K1,250.50", " 300 ", "ZMW 20", None])
    assert loader.to_number(s).tolist()[:3] == [1250.5, 300.0, 20.0]


def test_none_is_not_missing_by_default():
    df = pd.DataFrame({"tier": ["Gold", "None", "N/A", "Gold"]})
    out, _ = cleaning.clean(df, cleaning.CleaningOptions())
    assert out["tier"].isna().sum() == 0
    out, log = cleaning.clean(df, cleaning.CleaningOptions(placeholders_missing=True))
    assert out["tier"].isna().sum() == 1 and "None" in set(out["tier"])


def test_cleaning_log_counts():
    df = pd.DataFrame({"a": [" x", "x", "y", "y"], "n": [1.0, np.nan, 3.0, 3.0], "e": [np.nan] * 4})
    out, log = cleaning.clean(df, cleaning.CleaningOptions(numeric_missing="median"))
    steps = dict(zip(log["step"], log["affected"]))
    assert steps == {"Strip spaces": 1, "Empty columns": 1, "Duplicates": 1, "Fill numbers": 1}
    assert len(out) == 3 and out["n"].isna().sum() == 0
