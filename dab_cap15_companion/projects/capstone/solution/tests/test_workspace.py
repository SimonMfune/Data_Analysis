"""Unit tests for the workspace package. Run from this folder: python -m pytest tests"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workspace import data, insights, modelling, report  # noqa: E402
from workspace.llm_client import get_client  # noqa: E402

DB = data.SAMPLES / "kwacha_basket_sample.db"


@pytest.fixture(scope="module")
def churn():
    return data.run_select(DB, "SELECT * FROM customer_churn")


def test_sql_guard_blocks_changes():
    for bad in ["DELETE FROM customer_churn", "SELECT 1; DROP TABLE customer_churn", "UPDATE x SET y = 1"]:
        with pytest.raises(ValueError):
            data.run_select(DB, bad)
    assert len(data.run_select(DB, "WITH t AS (SELECT * FROM product_pricing) SELECT * FROM t")) == 600


def test_not_a_database_is_rejected():
    with pytest.raises(ValueError, match="not a SQLite database"):
        data.db_path_from_bytes(b"order_id,total\n1,2\n")


def test_logistic_matches_chapter_12(churn):
    r = modelling.fit(churn, "churned", ["recency_days", "orders_last_90d", "orders_last_180d",
                                         "tenure_days", "app_share"], "logistic")
    assert r.metrics["cv_auc_mean"] == pytest.approx(0.783, abs=0.001)    # Listing 12.10
    assert r.coefficients.iloc[0]["feature"] == "recency_days"


def test_linear_on_pricing():
    pr = data.run_select(DB, "SELECT * FROM product_pricing")
    r = modelling.fit(pr, "list_price_zmw", ["category", "brand_tier", "imported_flag", "weight_kg",
                                             "unit_cost_zmw"], "linear")
    assert r.metrics["test_r2"] > 0.9


def test_other_dataset_works():
    loans, _ = data.from_csv((data.SAMPLES / "fintech_loans.csv").read_bytes())
    assert modelling.suggest_kind(loans["defaulted"]) == "logistic"
    feats = [f for f in modelling.usable_features(loans, "defaulted") if f != "loan_id"]
    r = modelling.fit(loans, "defaulted", feats, "logistic")
    assert 0.5 < r.metrics["test_auc"] < 1


def test_insights_validation_accepts_honest_and_catches_careless(churn):
    r = modelling.fit(churn, "churned", ["recency_days", "orders_last_180d", "province"], "logistic")
    payload = insights.payload(churn, r)
    system, prompt = insights.prompt(payload, "The marketing manager")
    assert '"insight_request"' in prompt and "customer_id" not in prompt      # no rows are sent
    honest = get_client("mock").complete(prompt, system=system)
    reply, problems = insights.validate(honest.text, payload)
    assert reply is not None and problems == []
    careless = get_client("mock", mistakes=True).complete(prompt, system=system)
    _, problems = insights.validate(careless.text, payload)
    assert len(problems) >= 1


def test_invented_feature_is_caught(churn):
    r = modelling.fit(churn, "churned", ["recency_days", "orders_last_180d"], "logistic")
    payload = insights.payload(churn, r)
    fake = json.dumps({"recommendations": [{"title": "x", "detail": "y", "evidence": [r.metrics["test_auc"]],
                                            "features": ["shoe_size"]}],
                       "caveats": ["c"], "confidence": "low"})
    _, problems = insights.validate(fake, payload)
    assert any("shoe_size" in p for p in problems)


def test_report_contains_disclosure(churn):
    r = modelling.fit(churn, "churned", ["recency_days", "orders_last_180d"], "logistic")
    payload = insights.payload(churn, r)
    s, p = insights.prompt(payload, "Ms Banda")
    reply, problems = insights.validate(get_client("mock").complete(p, system=s).text, payload)
    md = report.build_markdown("test", churn, None, r, (reply, problems))
    assert "AI-generated draft" in md
    assert report.build_html(md, report.effects_chart_png(r)).startswith("<!DOCTYPE html>")
