d = pd.read_csv("data/clean/kb_delivery_times.csv", parse_dates=["order_datetime"])
late = d.groupby("province")["delayed_flag"].agg(["count", "mean"])
late["late_pct"] = late["mean"] * 100
print(late.drop(columns="mean").sort_values("late_pct", ascending=False).round(1))
print(f"Overall: {d['delayed_flag'].mean():.1%} late")
