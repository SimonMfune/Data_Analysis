with sqlite3.connect("data/kwacha_basket.db") as con:
    order_counts = pd.read_sql("""SELECT substr(order_datetime, 1, 7) AS month, COUNT(*) AS orders
                                  FROM orders WHERE status <> 'Cancelled' GROUP BY month""", con)
monthly["orders"] = order_counts.set_index(pd.to_datetime(order_counts["month"]))["orders"]
monthly["aov_zmw"] = monthly["revenue_zmw"] / monthly["orders"]
monthly["margin_pct"] = monthly["gross_margin_zmw"] / monthly["revenue_zmw"] * 100
monthly["returns_per_1000"] = monthly["returns"] / monthly["units"] * 1000

panels = [("orders", "Orders per month", "{x:,.0f}"),
          ("aov_zmw", "Average order value (K)", "K{x:,.0f}"),
          ("margin_pct", "Gross margin (%)", "{x:.0f}%"),
          ("returns_per_1000", "Returns per 1,000 units", "{x:.0f}")]

fig, axes = plt.subplots(2, 2, figsize=(9, 5.6), sharex=True, layout="constrained")
for ax, (column, title, fmt) in zip(axes.flat, panels):
    ax.plot(monthly.index, monthly[column])
    ax.set_title(title, fontsize=10)
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(0, monthly[column].max() * 1.15)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.suptitle("Orders more than doubled while margin and returns held steady",
             fontweight="bold", x=0.01, ha="left")
fig.savefig(FIG + "fig_8_11_subplots.png", dpi=200)
plt.close(fig)
first, last = monthly.loc["2023"].mean(), monthly.loc["2025"].mean()
print(pd.DataFrame({"2023": first, "2025": last})
      .loc[["orders", "aov_zmw", "margin_pct", "returns_per_1000"]].round(1))
