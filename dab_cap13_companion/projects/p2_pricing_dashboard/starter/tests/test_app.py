"""App tests with Streamlit's AppTest. Run from the solution folder: pytest tests"""
from pathlib import Path

from streamlit.testing.v1 import AppTest

HERE = Path(__file__).resolve().parents[1]


def run(path, **kw):
    return AppTest.from_file(str(HERE / path), default_timeout=60).run()


def test_home_suggests_guarded_price():
    at = run("views/suggest.py")
    at.number_input[0].set_value(12.0)          # unit cost
    at.number_input[1].set_value(0.2)           # weight
    at.selectbox[0].set_value("Stationery")
    at.button[0].click().run()
    assert not at.exception
    price = float(at.metric[0].value.replace("K", "").replace(",", ""))
    assert price >= 13.2                          # rule 1: never below cost + 10%


def test_home_default_matches_chapter_11():
    at = run("views/suggest.py")
    at.button[0].click().run()
    assert at.metric[0].value == "K66.00"


def test_navigation_shell_runs():
    at = run("app.py")
    assert not at.exception
    assert "Suggest a price" in at.title[0].value


def test_whatif_and_model_card_render():
    for page in ["views/what_if.py", "views/model_card.py"]:
        at = run(page)
        assert not at.exception, page


def test_batch_good_and_bad_files():
    at = run("views/batch.py")
    at.selectbox(key="batch_sample").set_value("new_products.csv").run()
    assert not at.exception and "Priced 12" in at.success[0].value
    at.selectbox(key="batch_sample").set_value("new_products_with_errors.csv").run()
    assert not at.exception
    assert "5 problem(s)" in at.error[0].value and "3 of 8 rows" in at.error[0].value
