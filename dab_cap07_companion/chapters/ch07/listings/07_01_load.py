customers = pd.read_csv("data/clean/kb_customer_demographics.csv",
                        dtype={"customer_id": str}, keep_default_na=False, na_values=[""])

query = """
SELECT o.order_id, o.customer_id, o.order_datetime, o.province, o.channel,
       p.method, p.amount_zmw
FROM orders AS o
JOIN payments AS p ON p.order_id = o.order_id
WHERE o.status <> 'Cancelled'
"""
with sqlite3.connect("data/kwacha_basket.db") as con:
    orders = pd.read_sql(query, con, parse_dates=["order_datetime"])

print(customers.shape, orders.shape)
print(orders["order_datetime"].min(), "to", orders["order_datetime"].max())
