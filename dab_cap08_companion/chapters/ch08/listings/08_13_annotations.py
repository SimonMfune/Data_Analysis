fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(monthly.index, monthly["revenue_zmw"])
ax.yaxis.set_major_formatter(FuncFormatter(kwacha))
ax.set_ylim(0, 5_400_000)

for year in [2023, 2024, 2025]:
    peak = pd.Timestamp(f"{year}-12-01")
    value = monthly.loc[peak, "revenue_zmw"]
    ax.annotate(f"December {year}\n{kwacha(value)}", xy=(peak, value),
                xytext=(-58, 14), textcoords="offset points", fontsize=8.5, ha="center",
                arrowprops={"arrowstyle": "-", "color": "#9AA5B1", "linewidth": 0.8})
ax.axvspan(pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31"), color="#0E9AA7", alpha=0.06)
ax.text(pd.Timestamp("2025-01-20"), 250_000, "2025: best year so far", fontsize=8.5, color="#4A5561")
ax.set_title("Each December peak was higher than the last")
ax.set_ylabel("Revenue")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.savefig(FIG + "fig_8_12_annotated.png", dpi=200)
plt.close(fig)
