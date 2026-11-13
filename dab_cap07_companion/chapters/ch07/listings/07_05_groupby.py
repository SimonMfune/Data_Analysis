by_age = (customers.groupby("age_band")
          .agg(customers=("customer_id", "count"),
               median_spend=("total_spend_zmw", "median"),
               mean_orders=("orders", "mean"),
               median_basket=("avg_basket_zmw", "median")))
print(by_age)

by_province = (customers.groupby("province")["total_spend_zmw"]
               .agg(["count", "median", "mean"])
               .sort_values("median", ascending=False))
print(by_province)
