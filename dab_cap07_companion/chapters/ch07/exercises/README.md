# Chapter 7 exercises

Run every script from the repository root, e.g. `python chapters/ch07/solutions/ex7_1_spend_profile.py`.

- **7.1 (Core)** Profile spending by age band and province from `data/clean/kb_customer_demographics.csv`.
  Report count, median and mean total spend per group, and write three findings, each with its number.
- **7.2 (Stretch)** Audit order values with the IQR rule. For each channel, report the fences, the number
  and share of outliers, and decide (with a reason) whether to keep, cap or drop them for a revenue report.
- **7.3 (Challenge)** Build your own RFM segmentation with `pd.qcut`. Produce a profile table with customer
  count, median recency, median orders and share of spend for each segment, and write three recommendations
  for Kwacha Basket's marketing team, each tied to a segment and a number.
