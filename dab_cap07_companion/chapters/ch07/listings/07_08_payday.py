orders["day"] = orders["order_datetime"].dt.day
calendar = pd.Series(pd.date_range("2023-01-01", "2025-12-31").day)
in_window = lambda day: (day >= 25) | (day <= 2)          # the 25th to the 2nd

orders_in = in_window(orders["day"]).sum()
days_in = in_window(calendar).sum()
print(f"Payday window: {orders_in / days_in:.1f} orders a day; "
      f"rest of month: {(len(orders) - orders_in) / (len(calendar) - days_in):.1f}")

per_day = orders["day"].value_counts().div(calendar.value_counts()).sort_index()
colours = ["#C9A227" if in_window(d) else "#0E9AA7" for d in per_day.index]
ax = per_day.plot.bar(figsize=(8, 3.4), color=colours, width=0.8)
ax.set_xlabel("Day of the month")
ax.set_ylabel("Orders per day")
plt.tight_layout()
plt.savefig(FIG + "fig_7_3_payday.png", dpi=200)
plt.close()
