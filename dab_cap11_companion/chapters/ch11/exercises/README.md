# Chapter 11 exercises

Run from the repository root, e.g. `python chapters/ch11/solutions/ex11_1_price_model.py`.

- **11.1 (Core)** Predict `list_price_zmw` in `data/clean/kb_product_pricing.csv` from category, brand tier,
  weight, unit cost and the imported flag. Use an 80/20 split with `random_state=2026`, a `Pipeline` with a
  `ColumnTransformer`, and report MAE and R² on the test set. Then suggest prices for three new products of
  your own design.
- **11.2 (Stretch)** Compare simple regression (unit cost only) with your multiple regression on the same split
  and with 5-fold cross-validation. Identify the three most influential features and explain them in plain
  language for a pricing manager who has never heard of regression.
- **11.3 (Challenge)** Use 5-fold cross-validation to compare plain linear regression with Ridge regression at
  several values of alpha, for both the plain and the log-log model. Choose a final model, evaluate it once on
  the test set, and write a one-page model summary (purpose, data, features, performance, limitations, how to
  use it) in Markdown.
