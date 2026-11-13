# Project 2 solution: Price Advisor

    cd projects/p2_pricing_dashboard/solution
    python train.py                  # trains, evaluates and saves artefacts/price_model.joblib
    streamlit run app.py
    python -m pytest tests           # 16 tests: rules, validation, artefact and every page

Training (`train.py`) and serving (`app.py`, `views/`, `serving.py`) are separate: the app only loads
the saved artefact. Model files are not committed; run `train.py` after cloning or upgrading scikit-learn.
`ai_review_example.md` is a worked AI code review against the Section 13.7 checklist.
