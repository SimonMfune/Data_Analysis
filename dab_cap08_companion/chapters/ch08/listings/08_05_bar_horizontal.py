y2025 = kpis[kpis["month"].dt.year == 2025]
province = y2025.groupby("province")["revenue_zmw"].sum().sort_values() / 1e6

fig, ax = plt.subplots(figsize=(8, 4.2))
bars = ax.barh(province.index, province.values, color="#0E9AA7", height=0.7)
ax.bar_label(bars, fmt="K%.2fm", padding=4, fontsize=9)
ax.set_title("Lusaka and the Copperbelt produced almost 60% of 2025 revenue")
ax.set_xlabel("Revenue, 2025 (K million)")
ax.grid(axis="y", visible=False)
ax.grid(axis="x", visible=True)
ax.margins(x=0.12)
fig.savefig(FIG + "fig_8_5_bar_horizontal.png", dpi=200)
plt.close(fig)
share = province[["Lusaka", "Copperbelt"]].sum() / province.sum()
print(f"Lusaka + Copperbelt share of 2025 revenue: {share:.1%}")
