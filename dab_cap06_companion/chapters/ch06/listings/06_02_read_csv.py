messy = pd.read_csv("data/raw/kb_orders_messy.csv")
print(messy.shape)
print(messy[["order_id", "order_date", "province", "items", "total"]].head())
print(messy.dtypes)
