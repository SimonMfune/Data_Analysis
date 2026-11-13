# Chapter 15 answers

## Check Your Understanding 15.1
1. A dataset; then data prepared from it; then a model of the prepared data; then insights from that model. Each depends on the one before.
2. Because a model fitted to the old data would otherwise be shown, explained and reported as if it belonged to the new data.

## Check Your Understanding 15.2
1. A read-only connection (`mode=ro`), a single statement, and a check that it starts with SELECT or WITH; results are also capped at 200,000 rows.
2. With the SQL wrapped in `SELECT * FROM (...) LIMIT`, a statement that is not a query fails, and the row cap protects memory.

## Check Your Understanding 15.3
1. Logistic regression: the target has two values. The positive class is the later of the two values in sorted order (1 for churned).
2. `st.cache_data` stores the result for each combination of data, target, features and model, so moving the threshold slider does not refit.

## Check Your Understanding 15.4
1. Grounding (only computed figures are sent), validation (schema, numbers and features checked), disclosure (the text is labelled AI-generated).
2. The page shows the problems and the report leaves the recommendations out.

## Check Your Understanding 15.5
1. In the app's Secrets in Community Cloud's Advanced settings (or app settings after deployment); locally in `.streamlit/secrets.toml` or `.env`, both ignored by Git.
2. The Python version you tested with, the secrets, and the main file path.

## Acceptance exercise
The solution passes `python -m pytest tests` (10 tests), including the full six-page flow on both datasets.
Deployment cannot be tested automatically: follow `DEPLOY.md`, then run the demo script on the public URL.
