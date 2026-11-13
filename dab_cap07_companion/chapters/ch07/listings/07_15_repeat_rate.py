o = orders.sort_values("order_datetime")
o["n"] = o.groupby("customer_id").cumcount() + 1
first = o[o["n"] == 1].set_index("customer_id")["order_datetime"]
second = o[o["n"] == 2].set_index("customer_id")["order_datetime"]
gap = (second.reindex(first.index) - first).dt.days

cohort = pd.DataFrame({"first": first, "repeat_90d": gap < 91})
cohort = cohort[cohort["first"] < "2025-10-01"]
rate = cohort.groupby(cohort["first"].dt.to_period("Q"))["repeat_90d"].mean().mul(100)
print(rate.round(1).to_string())
