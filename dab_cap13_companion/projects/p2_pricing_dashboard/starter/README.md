# Project 2 starter: Price Advisor

    cd projects/p2_pricing_dashboard/starter
    python train.py                  # M1: fails until train.py is written
    streamlit run app.py
    python -m pytest tests           # fails until every milestone is finished; that is the target

| Milestone | Section | Files | Done when |
|---|---|---|---|
| M1 Train and persist | 13.3 | `train.py` | `artefacts/price_model.joblib` holds the model, interval and metrics |
| M2 One product, with an interval | 13.4 | `serving.py`, `guardrails.py`, `views/suggest.py` | K45 Value grocery, 2 kg, local → K66.00 |
| M3 What-if and margin | 13.5 | `views/what_if.py` | Tier table and cost chart respond to every control |
| M4 Model card | 13.6 | `views/model_card.py` | Metrics, residual plot, effects and limitations shown |
| M5 Batch scoring | 13.7 | `validation.py`, `views/batch.py` | Good file priced; bad file gives one message per bad row |

`features.py` (the Chapter 11 model) and `app.py` (navigation) are complete.
