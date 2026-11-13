"""Unit tests for guardrails, validation and the saved artefact. Run from the solution folder: pytest tests"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from guardrails import apply_guardrails, round_to_ending  # noqa: E402
from serving import load_artefact, suggest  # noqa: E402
from validation import validate_batch  # noqa: E402


@pytest.mark.parametrize("price, expected", [(66.24, 66.00), (66.30, 66.50), (66.80, 66.99),
                                             (2729.61, 2729.50), (9.97, 9.99)])
def test_round_to_ending(price, expected):
    assert round_to_ending(price) == expected


def test_never_below_cost_plus_ten_percent():
    price, notes = apply_guardrails(model_price=3.23, unit_cost=12.0)
    assert price >= 13.2 and notes
    for cost in np.linspace(5, 5000, 200):
        assert apply_guardrails(cost * 0.9, cost)[0] >= cost * 1.10 - 1e-9


def test_artefact_matches_chapter_11():
    art = load_artefact()
    row = pd.DataFrame([{"category": "Groceries", "brand_tier": "Value", "imported_flag": 0,
                         "weight_kg": 2.0, "unit_cost_zmw": 45.0}])
    out = suggest(art, row).iloc[0]
    assert out["model_price_zmw"] == pytest.approx(66.24, abs=0.01)
    assert out["low_zmw"] < out["model_price_zmw"] < out["high_zmw"]
    assert out["suggested_price_zmw"] == 66.00


def test_interval_coverage_close_to_80_percent():
    cov = load_artefact()["metrics"]["interval_coverage_test"]
    assert 0.70 <= cov <= 0.90


def test_validation_accepts_good_file():
    good, problems = validate_batch(pd.read_csv(HERE / "sample_data" / "new_products.csv"))
    assert problems == [] and len(good) == 12


def test_validation_reports_each_bad_row():
    good, problems = validate_batch(pd.read_csv(HERE / "sample_data" / "new_products_with_errors.csv"))
    assert len(good) == 3
    text = " ".join(problems)
    for expected in ["Row 3: unit_cost_zmw must be a number", "Row 4: category 'Toys'",
                     "Row 5: weight_kg = -1", "Row 6: imported_flag must be a number",
                     "Row 7: brand_tier 'Luxury'"]:
        assert expected in text


def test_missing_column_is_fatal():
    good, problems = validate_batch(pd.DataFrame({"category": ["Groceries"], "unit_cost_zmw": [10]}))
    assert good.empty and problems[0].startswith("Missing column(s)")
