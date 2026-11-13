cols = ["age", "tenure_days", "orders", "total_spend_zmw", "avg_basket_zmw",
        "recency_days", "returns_count"]
pearson = customers[cols].corr(method="pearson")
spearman = customers[cols].corr(method="spearman")
print(pearson.loc[["orders", "returns_count", "recency_days"],
                  ["total_spend_zmw", "returns_count", "age"]].round(2))
print(f"Spend vs orders: Pearson {pearson.loc['orders', 'total_spend_zmw']:.2f}, "
      f"Spearman {spearman.loc['orders', 'total_spend_zmw']:.2f}")

per_order = customers["returns_count"] / customers["orders"]
print(f"Returns per order vs spend, Spearman: "
      f"{per_order.corr(customers['total_spend_zmw'], method='spearman'):.2f}")
