# Chapter 9 answers

## Check Your Understanding 9.1
1. It can be tested without Streamlit, reused in another app or notebook, and changed without touching the layout. `app.py` only arranges widgets and calls functions.
2. Because AppTest cannot upload files; the sample selector gives tests (and new users) a way in.

## Check Your Understanding 9.2
1. Reading as text loses nothing: leading zeros, "None", phone numbers and odd dates survive, and every conversion is then a deliberate, logged decision.
2. latin-1 maps every byte to a character, so it never fails; it is the last resort that guarantees the file opens, but may show the wrong characters for a few bytes.

## Check Your Understanding 9.3
1. Some files use "None" or "N/A" as a real value (Chapter 4's loyalty tier). Turning them into missing values silently would destroy data.
2. Streamlit hashes a function's arguments to find a cached result. A frozen dataclass cannot change after creation, so the same options always mean the same result.

## Check Your Understanding 9.4
1. Each new file has different columns; a chart choice remembered from the old file could name a column that no longer exists.
2. `st.cache_data` stores the return value and hands each caller a copy, so later code cannot change the cached result by accident.

## Acceptance exercise
Run `python -m pytest tests` in the solution folder (15 tests) and work through Table 9.1 by hand with
`data/raw/kb_orders_messy.csv` uploaded: 8,190 rows read, 200 values stripped, 151 duplicates dropped,
8,039 rows left.

## Extension exercise
`solutions/ext_correlation_heatmap.py` shows a correlation heatmap. For an outlier tab, reuse the IQR rule
from Section 7.5 per number column; for a PDF summary, save the figures with `charts.save(..., "x.pdf")` and
combine them with `matplotlib.backends.backend_pdf.PdfPages`.
