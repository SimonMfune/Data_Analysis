# Chapter 12 exercises

Run from the repository root, e.g. `python chapters/ch12/solutions/ex12_1_churn_model.py`.

- **12.1 (Core)** Predict `churned` in `data/clean/kb_customer_churn.csv` with logistic regression. Use a
  stratified 75/25 split with `random_state=2026`, handle the missing ratings, and report the confusion matrix
  with accuracy, precision, recall and F1 at the 0.5 threshold, with and without `class_weight="balanced"`.
- **12.2 (Stretch)** Ms Banda proposes a cheaper retention offer: a K80 delivery-fee waiver that keeps 20% of
  real churners. Using the chapter's estimate of the margin at risk, choose the threshold that maximises net
  benefit using out-of-fold predictions on the training set only, then report the result on the test set and
  compare with the K150 voucher.
- **12.3 (Challenge)** Audit the model's performance across provinces and gender with out-of-fold
  predictions. Add bootstrap 95% confidence intervals to recall and precision for each group, identify any
  gaps that are larger than chance, and write three recommendations.
