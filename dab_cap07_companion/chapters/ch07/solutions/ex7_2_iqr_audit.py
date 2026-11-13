"""Exercise 7.2 solution: IQR outlier audit of order values, by channel."""
import sqlite3

import pandas as pd

with sqlite3.connect("data/kwacha_basket.db") as con:
    o = pd.read_sql("""SELECT o.order_id, o.channel, p.amount_zmw FROM orders o
                       JOIN payments p ON p.order_id = o.order_id
                       WHERE o.status <> 'Cancelled'""", con)

def audit(values):
    q1, q3 = values.quantile([0.25, 0.75])
    high = q3 + 1.5 * (q3 - q1)
    flagged = values > high
    return pd.Series({"upper_fence": high, "outliers": flagged.sum(),
                      "share_pct": flagged.mean() * 100,
                      "revenue_share_pct": values[flagged].sum() / values.sum() * 100})

print(o.groupby("channel")["amount_zmw"].apply(audit).unstack().round(1))
print("\nDecision: keep them. They are real high-value orders (phones, solar kits) and carry")
print("a large share of revenue; dropping or capping them would understate revenue.")
print("For a model of basket size, consider modelling log(order value) or analysing the")
print("high-value orders separately; capping is acceptable there only if documented.")
