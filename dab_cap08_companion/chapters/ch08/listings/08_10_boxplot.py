deliveries = pd.read_csv("data/clean/kb_delivery_times.csv")
order = deliveries.groupby("province")["delivery_hours"].median().sort_values().index
data = [deliveries.loc[deliveries["province"] == p, "delivery_hours"] for p in order]

fig, ax = plt.subplots(figsize=(8, 4.4))
ax.boxplot(data, tick_labels=order, orientation="horizontal", widths=0.6,
           patch_artist=True, showfliers=False,
           boxprops={"facecolor": "#BFE6E9", "edgecolor": "#0E9AA7"},
           medianprops={"color": "#1B2A41", "linewidth": 1.6},
           whiskerprops={"color": "#9AA5B1"}, capprops={"color": "#9AA5B1"})
ax.set_title("Delivery times rise with distance from Kwacha Basket's hubs")
ax.set_xlabel("Hours from order to delivery (outliers hidden)")
ax.grid(axis="y", visible=False)
ax.grid(axis="x", visible=True)
fig.savefig(FIG + "fig_8_10_boxplot.png", dpi=200)
plt.close(fig)
print(deliveries.groupby("province")["delivery_hours"].median().sort_values().round(1))
