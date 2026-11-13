# Chapter 6 exercises

**6.1 (Core).** Write your own `clean_orders.py` for `data/raw/kb_orders_messy.csv` that writes a clean CSV and
a cleaning log. Compare it with `../clean_orders.py`, then run `../solutions/check_against_truth.py` against
your output to see how many values you recovered correctly.

**6.2 (Stretch).** Produce a data-quality report (completeness, validity and uniqueness by column) before and
after cleaning. Model answer: `../solutions/ex6_2_quality_report.py`.

**6.3 (Challenge).** Write pytest tests for each cleaning function, including edge cases. Model answer:
`../tests/test_clean_orders.py` (run `pytest chapters/ch06/tests -v`).
