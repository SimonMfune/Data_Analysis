# Chapter 13 answers

## Check Your Understanding 13.1
1. Training is slow, needs the full dataset and should happen deliberately; serving must be fast and must never change the model. Keeping them apart also means the app can run where the training data is not available.
2. The model, the interval quantiles, the metrics, the effects, the test predictions, the cost range, the training date and the library versions: everything a page needs, so no page has to recompute anything.

## Check Your Understanding 13.2
1. Quantiles of residuals measured on data the model did not see while it was fitted (out-of-fold). In-sample residuals are too small and would give an interval that is too narrow.
2. 120 test products give a coverage estimate with a standard error of about 4 percentage points, so 75% is consistent with a true 80%; it is a warning to watch, not proof of a fault.

## Check Your Understanding 13.3
1. Rule 1 is applied first, then rounding with the floor as a minimum, so rounding can never take a price back below cost + 10%.
2. In `serving.suggest`, which every page calls, so no page can skip it.

## Check Your Understanding 13.4
1. `st.cache_resource` keeps one shared object per server process (right for a model that is read but never changed); `st.cache_data` returns a fresh copy to every caller (right for DataFrames that a page may modify).
2. A clear message naming the row, the column, the value and the rule lets a user fix the file without help.

## Acceptance exercise
- Predictions match the saved model: `test_artefact_matches_chapter_11` and `test_home_default_matches_chapter_11` (K66.24 → K66.00).
- Interval coverage on the test set: 75.0% for a nominal 80% (Section 13.4 discusses why).
- Batch upload: `new_products_with_errors.csv` gives five row-numbered messages and prices the three good rows.

## Extension exercise
For a price-sensitivity chart, the What-if page already plots price against cost by tier; add a second chart of
margin % against suggested price. For competitor prices, add an optional `competitor_price_zmw` column to the
batch file and flag suggestions more than 10% above it. For retraining, add a page that runs `train.main()` only
for an authorised user and shows the old and new metrics side by side before replacing the artefact.
