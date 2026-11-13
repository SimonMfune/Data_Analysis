by_cat = kpis.pivot_table(index="month", columns="category", values="revenue_zmw", aggfunc="sum")
lines = pd.DataFrame({
    "Electronics": by_cat["Electronics"],
    "Other seven categories": by_cat.drop(columns="Electronics").sum(axis=1),
}).rolling(3).mean() / 1e6                 # a three-month average smooths monthly noise

fig, ax = plt.subplots(figsize=(8, 4.2))
for name, offset in zip(lines.columns, [8, -8]):
    ax.plot(lines.index, lines[name], label=name)
    ax.annotate(name, xy=(lines.index[-1], lines[name].iloc[-1]), xytext=(6, offset),
                textcoords="offset points", va="center", fontsize=9)
ax.set_title("Electronics earns a third of all revenue, and its share is edging up")
ax.set_ylabel("Revenue, 3-month average (K million)")
ax.set_ylim(0, None)
ax.legend(loc="upper left")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_xlim(right=lines.index[-1] + pd.Timedelta(days=170))   # room for the labels
fig.savefig(FIG + "fig_8_4_line_categories.png", dpi=200)
plt.close(fig)
year = by_cat.groupby(by_cat.index.year).sum()
print((year["Electronics"] / year.sum(axis=1) * 100).round(1).rename("Electronics share (%)"))
