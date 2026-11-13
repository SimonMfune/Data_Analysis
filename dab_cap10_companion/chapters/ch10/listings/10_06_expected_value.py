with sqlite3.connect("data/kwacha_basket.db") as con:
    lines = pd.read_sql("""SELECT i.order_id, COUNT(*) AS lines FROM order_items i
                           JOIN orders o ON o.order_id = i.order_id
                           WHERE o.status <> 'Cancelled' GROUP BY i.order_id""", con)["lines"]
pmf = lines.value_counts(normalize=True).sort_index()
print(pmf.round(3).to_string())
ev = (pmf.index * pmf).sum()
var = ((pmf.index - ev) ** 2 * pmf).sum()
print(f"E[X] = {ev:.3f} product lines per order;  Var(X) = {var:.3f};  SD = {var ** 0.5:.3f}")
print(f"Check with pandas: mean {lines.mean():.3f}, SD {lines.std(ddof=0):.3f}")
