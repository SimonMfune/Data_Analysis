# Project 1 solution: Quick EDA

    cd projects/p1_eda_dashboard/solution
    streamlit run app.py
    python -m pytest tests          # 15 tests: modules plus the whole app via AppTest

Modules: `app.py` (layout and state only), `loader.py` (M1), `profiling.py` (M2),
`cleaning.py` (M3), `charts.py` (M4, built on Chapter 8's `shared/charts.py`).
`ai_log_example.md` is a worked AI pair-programming log for Milestone M4.
The folder is self-contained (it carries its own `kb.mplstyle`), so it can be deployed
to Streamlit Community Cloud as it is (Chapter 15).
