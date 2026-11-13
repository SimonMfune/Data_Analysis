print("Exact duplicate rows:", messy.duplicated().sum())
print("Repeated order IDs:  ", messy["order_id"].duplicated().sum())

near = messy[messy["order_id"].duplicated(keep=False) & ~messy.duplicated(keep=False)]
pair = near[near["order_id"] == near["order_id"].iloc[0]]
print(pair[["order_id", "customer_id", "channel", "province"]].map(repr))
