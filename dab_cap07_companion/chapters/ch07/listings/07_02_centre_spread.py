spend = customers["total_spend_zmw"]
print(spend.describe())
print(f"Mean K{spend.mean():,.0f}  Median K{spend.median():,.0f}  Skew {spend.skew():.2f}")
print(f"IQR: K{spend.quantile(0.75) - spend.quantile(0.25):,.0f}")
top10 = spend.sort_values(ascending=False).head(int(len(spend) * 0.10)).sum() / spend.sum()
print(f"Top 10% of customers account for {top10:.1%} of all spending")
