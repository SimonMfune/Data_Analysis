print(f"{len(churn):,} customers active at 30 September 2025; "
      f"{churn['churned'].sum()} churned in the next 90 days ({churn['churned'].mean():.1%})")

bands = pd.cut(churn["recency_days"], [-1, 14, 30, 60, 90, 180],
               labels=["0-14", "15-30", "31-60", "61-90", "91-180"])
print(churn.groupby(bands, observed=True)["churned"].agg(customers="count", churn_rate="mean")
      .round(3).rename_axis("days since last order").to_string())
