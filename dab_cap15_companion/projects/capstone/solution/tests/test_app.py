"""The whole workspace, page by page, with Streamlit's AppTest. Run from this folder: python -m pytest tests"""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_full_flow_with_the_kwacha_basket_database():
    at = AppTest.from_file(APP, default_timeout=120).run()
    assert not at.exception
    at.selectbox(key="data_table").set_value("customer_churn").run()
    at.button[0].click().run()                                   # Run query and use the result
    assert "customer_churn" in at.session_state["dataset"]["name"]
    for page in ["views/prepare.py", "views/explore.py"]:
        at.switch_page(page).run()
        assert not at.exception, page
    at.switch_page("views/model.py").run()
    at.selectbox(key="m_target").set_value("churned").run()
    assert not at.exception
    assert at.session_state["model"].kind == "logistic"
    before = at.metric[4].value                                   # precision at 0.50
    at.slider(key="m_threshold").set_value(0.3).run()             # metrics update live
    assert at.metric[4].value != before
    at.switch_page("views/insights.py").run()
    at.button[0].click().run()                                    # Generate recommendations (mock)
    assert not at.exception
    assert at.session_state["insights"]["problems"] == []
    at.switch_page("views/report.py").run()
    assert not at.exception
    assert any("AI-generated draft" in m.value for m in at.markdown)


def test_second_dataset_fintech_loans():
    at = AppTest.from_file(APP, default_timeout=120).run()
    at.radio(key="data_source").set_value("Sample: fintech loans CSV").run()
    at.button[0].click().run()
    at.switch_page("views/prepare.py").run()
    at.switch_page("views/model.py").run()
    at.selectbox(key="m_target").set_value("defaulted").run()
    assert not at.exception
    assert at.session_state["model"].target == "defaulted"
