# Chapter 14 · AI in the Data Analysis Workflow

    python chapters/ch14/run_session.py               # Listings 14.1-14.12 with the offline mock provider
    python chapters/ch14/figures/ch14_figures.py      # Figures 14.1 and 14.2
    python -m pytest chapters/ch14/tests              # tests for shared/llm_client.py (no network needed)

Everything runs offline by default. To use a live model, copy `.env.example` to `.env` in the repository
root and set `LLM_PROVIDER` (openai, anthropic or google), `LLM_MODEL` (a current model name from that
provider's model list) and the matching API key. Never commit `.env`.

Outputs printed in the book come from the mock provider. With a live model, the numbers computed in
pandas are identical; the wording of replies, and the label counts in Listings 14.10-14.12, will differ.

| Folder | Contents |
|---|---|
| `listings/`, `outputs/` | Listings 14.1-14.12, their output, and `human_check_sample.csv` |
| `figures/` | Figures 14.1-14.3 |
| `exercises/`, `solutions/` | Exercise briefs, solutions and `ch14_answers.md` |
| `tests/` | Offline tests for the provider adapters, retries and cache |
