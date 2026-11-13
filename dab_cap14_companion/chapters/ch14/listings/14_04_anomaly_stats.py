kpis = pd.read_csv("data/clean/kb_monthly_kpis.csv")
monthly = kpis.pivot_table(index="month", columns="province", values="revenue_zmw", aggfunc="sum")

def anomaly_summary(monthly, month, threshold=2.0):
    """Compact statistics for one month: each province against its own previous 12 months."""
    history = monthly.loc[:month].iloc[-13:-1]               # the 12 months before `month`
    current = monthly.loc[month]
    # compare with the trend: last month's level, and the spread of month-on-month changes
    changes = history.pct_change().dropna()
    expected = history.iloc[-1] * (1 + changes.mean())
    z = (current / expected - 1) / changes.std()
    flagged = z[z.abs() >= threshold].sort_values()
    total, previous = current.sum(), monthly.loc[:month].iloc[-2].sum()
    return {
        "period": pd.Period(month).strftime("%B %Y"),
        "total_revenue_zmw": round(float(total), 2),
        "change_vs_previous_pct": round(float((total / previous - 1) * 100), 1),
        "method": "each province vs its own trend over the previous 12 months; flag |z| >= 2",
        "anomalies": [{"province": p, "revenue_zmw": round(float(current[p]), 2),
                       "change_vs_typical_pct": round(float((current[p] / expected[p] - 1) * 100), 1),
                       "z_score": round(float(z[p]), 2)} for p in flagged.index],
    }

stats = anomaly_summary(monthly, "2025-01")
print(json.dumps(stats, indent=2))
print(f"\nAbout {estimate_tokens(json.dumps(stats))} tokens, instead of "
      f"{estimate_tokens(kpis.to_csv(index=False)):,} for the raw KPI file")
