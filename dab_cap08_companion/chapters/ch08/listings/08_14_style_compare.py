def category_bars(ax):
    totals = kpis.groupby("category")["revenue_zmw"].sum().sort_values() / 1e6
    ax.barh(totals.index, totals.values)
    ax.set_title("Revenue by category, 2023-2025")
    ax.set_xlabel("K million")

fig = plt.figure(figsize=(10, 3.6), layout="constrained")
with plt.style.context("default"):         # Matplotlib's own defaults, temporarily
    category_bars(fig.add_subplot(1, 2, 1))
with plt.style.context("shared/kb.mplstyle"):
    ax = fig.add_subplot(1, 2, 2)
    category_bars(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
fig.savefig(FIG + "fig_8_13_style_compare.png", dpi=200)
plt.close(fig)
print(plt.rcParams["axes.prop_cycle"].by_key()["color"])
