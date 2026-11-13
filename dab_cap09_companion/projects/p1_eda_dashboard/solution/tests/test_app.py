"""End-to-end tests with Streamlit's AppTest. Run from the solution folder: pytest tests"""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")
SAMPLES = ["clinic_visits.csv", "fintech_loans.csv", "marketing_leads.csv"]


def start(sample):
    at = AppTest.from_file(APP, default_timeout=60).run()
    at.selectbox(key="sample").set_value(sample).run()
    assert not at.exception, at.exception
    return at


def test_welcome_screen():
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception
    assert "Upload a CSV file" in at.info[0].value


@pytest.mark.parametrize("sample", SAMPLES)
def test_every_sample_and_chart(sample):
    at = start(sample)
    assert at.title[0].value == sample
    kinds = at.radio(key="chart_kind").options
    for kind in kinds:                         # every chart type the file allows must draw
        at.radio(key="chart_kind").set_value(kind).run()
        assert not at.exception, (sample, kind, at.exception)


def test_cleaning_options_change_result():
    at = start("fintech_loans.csv")
    rows_before = at.metric[0].value
    at.selectbox(key="opt_numeric").set_value("drop rows").run()
    assert not at.exception
    assert at.metric[0].value != rows_before


def test_switching_file_resets_chart_choices():
    at = start("fintech_loans.csv")
    at.radio(key="chart_kind").set_value("Scatter").run()
    at.selectbox(key="sample").set_value("clinic_visits.csv").run()
    assert not at.exception
    assert at.radio(key="chart_kind").value == "Histogram"
