# Project 1 starter: Quick EDA

    cd projects/p1_eda_dashboard/starter
    streamlit run app.py
    python -m pytest tests          # fails until every milestone is finished; that is the target

| Milestone | Section | Files | Done when |
|---|---|---|---|
| M1 Upload and robust loading | 9.3 | `loader.py`, `app.py` | All three `data/unseen` files load with the right encoding and delimiter |
| M2 Profiling | 9.4 | `profiling.py`, `app.py` | Profile table matches pandas; metrics show at the top |
| M3 Configurable cleaning | 9.5 | `cleaning.py`, `app.py` | Every option works and the log counts each change |
| M4 Summary and charts | 9.6 | `charts.py`, `app.py` | Every chart type draws for every sample file |
| M5 Performance, download, polish | 9.7 | `app.py` | Cached, downloads work, file switching resets chart choices |

Keep `ai_log.md` up to date for the milestone where you pair with an AI assistant (Section 9.6).
