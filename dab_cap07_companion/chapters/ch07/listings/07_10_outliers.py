values = orders["amount_zmw"]
q1, q3 = values.quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = orders[(values < low) | (values > high)]
print(f"Q1 K{q1:,.2f}  Q3 K{q3:,.2f}  IQR K{iqr:,.2f}  upper fence K{high:,.2f}")
print(f"IQR outliers: {len(outliers):,} orders ({len(outliers) / len(orders):.1%})")

z = (values - values.mean()) / values.std()
print(f"|z| > 3: {(z.abs() > 3).sum():,} orders")

with sqlite3.connect("data/kwacha_basket.db") as con:
    has_phone = pd.read_sql("""SELECT DISTINCT i.order_id FROM order_items i
                               JOIN products p ON p.product_id = i.product_id
                               WHERE p.subcategory IN ('Mobile Phones', 'Solar & Power')""", con)
share = outliers["order_id"].isin(has_phone["order_id"]).mean()
print(f"Outlier orders containing a phone or solar product: {share:.1%}")
