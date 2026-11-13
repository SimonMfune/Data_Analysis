with sqlite3.connect("data/kwacha_basket.db") as con:
    t = pd.read_sql("SELECT order_datetime FROM orders WHERE status <> 'Cancelled' "
                    "AND order_datetime LIKE '2025-0%'", con, parse_dates=["order_datetime"])["order_datetime"]
evening = t[(t.dt.hour == 20) & t.dt.month.isin([6, 7, 8]) & t.dt.day.between(3, 24)]
days = pd.date_range("2025-06-01", "2025-08-31")
days = days[(days.day >= 3) & (days.day <= 24)]
counts = evening.dt.normalize().value_counts().reindex(days, fill_value=0)
lam = counts.mean()
print(f"Orders between 20:00 and 21:00, {len(days)} non-payday days, June-August 2025")
print(f"mean = {lam:.2f}, variance = {counts.var():.2f}  (Poisson: mean = variance)")
P = stats.poisson(lam)
print(f"P(10 or more orders in that hour) = {1 - P.cdf(9):.3f};  observed {(counts >= 10).mean():.3f}")
