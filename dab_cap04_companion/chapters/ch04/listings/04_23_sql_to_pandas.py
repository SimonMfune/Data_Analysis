"""Listing 4.23 — run a SQL query from Python and receive a pandas DataFrame."""
import sqlite3

import pandas as pd

query = """
SELECT strftime('%Y', o.order_datetime) AS year,
       o.channel,
       ROUND(SUM(i.quantity * i.unit_price_zmw), 2) AS revenue_zmw
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY year, o.channel
"""

with sqlite3.connect("data/kwacha_basket.db") as con:
    df = pd.read_sql(query, con)

table = df.pivot(index="year", columns="channel", values="revenue_zmw")
print(table)
print()
print("Share of 2025 revenue by channel:")
print((table.loc["2025"] / table.loc["2025"].sum() * 100).round(1))
