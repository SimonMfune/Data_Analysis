kpis["year"] = kpis["month"].dt.year
top = kpis.groupby("category")["revenue_zmw"].sum().nlargest(3).index
grouped = (kpis[kpis["category"].isin(top)]
           .pivot_table(index="category", columns="year", values="revenue_zmw", aggfunc="sum")
           .loc[top] / 1e6)

x = np.arange(len(grouped))               # one position per category
width = 0.26
fig, ax = plt.subplots(figsize=(8, 4))
for i, year in enumerate(grouped.columns):
    ax.bar(x + (i - 1) * width, grouped[year], width, label=str(year))
ax.set_xticks(x, grouped.index)
ax.set_title("Each of the top three categories grew year on year")
ax.set_ylabel("Revenue (K million)")
ax.legend(title="Year", ncols=3, loc="upper right")
fig.savefig(FIG + "fig_8_6_bar_grouped.png", dpi=200)
plt.close(fig)
print(grouped.round(2))
