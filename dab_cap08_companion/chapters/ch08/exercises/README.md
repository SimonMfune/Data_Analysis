# Chapter 8 exercises

Run from the repository root, e.g. `python chapters/ch08/solutions/ex8_1_four_panel.py`.

- **8.1 (Core)** Build a four-panel visual report of how Kwacha Basket changed from 2023 to 2025, using
  `data/clean/kb_monthly_kpis.csv`. Each panel needs a title that states its finding, labelled units and the
  house style. Save it as a 300-dpi PNG and as an SVG.
- **8.2 (Stretch)** Annotate a monthly revenue chart with the three most important events you can find in the
  data: the December 2025 peak, the largest month-on-month fall, and the month of the campaign with the largest
  budget (`data/clean/campaigns.csv`). Find each event with code, not by eye.
- **8.3 (Challenge)** Write `charts.py`, a library of reusable, styled chart functions with docstrings, and
  tests for it. Rebuild your Exercise 8.1 report with it. The model answer is `shared/charts.py`, with tests
  in `chapters/ch08/tests/test_charts.py`.
