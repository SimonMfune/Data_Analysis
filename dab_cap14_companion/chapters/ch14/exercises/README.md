# Chapter 14 exercises

Run from the repository root, e.g. `python chapters/ch14/solutions/ex14_1_anomaly_summary.py`.
Every solution runs with the offline mock provider. Set `LLM_PROVIDER`, `LLM_MODEL` and one API key in
`.env` to run it against a live model.

- **14.1 (Core)** Write a script that computes anomaly statistics for a slice of sales data (one category's
  monthly revenue by province), sends them to a model, and returns a plain-language summary. Compare each month
  with the same month a year earlier, so that the January dip after the festive season is not flagged, and
  cross-check every number in the reply.
- **14.2 (Stretch)** Extract themes and sentiment from all 1,000 reviews to the validated JSON schema of
  Listing 14.9, and chart the share of reviews mentioning each theme by category.
- **14.3 (Challenge)** Send the same prompt to every provider you have a key for, score each reply against a
  rubric, and report the trade-offs in cost, latency and accuracy.
