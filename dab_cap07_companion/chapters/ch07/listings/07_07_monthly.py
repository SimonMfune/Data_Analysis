monthly = orders.set_index("order_datetime").resample("MS")["amount_zmw"].agg(["count", "sum"])
monthly.columns = ["orders", "revenue_zmw"]
print(monthly.tail(4))

m2025 = monthly.loc["2025"]
print(f"December 2025 revenue is {m2025['revenue_zmw'].iloc[-1] / m2025['revenue_zmw'].iloc[:-1].mean():.2f}"
      " times the average of the other 2025 months")

ax = monthly["revenue_zmw"].div(1e6).plot(figsize=(8, 3.6), marker="o", ms=3, color="#0E9AA7")
ax.set_ylabel("Revenue (K million)")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig(FIG + "fig_7_2_monthly_revenue.png", dpi=200)
plt.close()
