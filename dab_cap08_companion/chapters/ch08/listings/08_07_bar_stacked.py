mix = kpis.pivot_table(index="year", columns="category", values="revenue_zmw", aggfunc="sum")
mix = mix[list(top)].assign(Other=mix.drop(columns=top).sum(axis=1))
share = mix.div(mix.sum(axis=1), axis=0) * 100           # each year's mix sums to 100%

fig, ax = plt.subplots(figsize=(8, 3.2))
left = np.zeros(len(share))
for name in share.columns:
    ax.barh(share.index.astype(str), share[name], left=left, label=name, height=0.6)
    for y, (start, width) in enumerate(zip(left, share[name])):
        ax.text(start + width / 2, y, f"{width:.0f}%", ha="center", va="center",
                color="white", fontsize=9, fontweight="bold")
    left += share[name].to_numpy()
ax.set_title("The category mix barely changed between years")
ax.set_xlabel("Share of revenue (%)")
ax.set_xlim(0, 100)
ax.invert_yaxis()                                          # 2023 at the top
ax.grid(False)
ax.legend(ncols=5, loc="upper center", bbox_to_anchor=(0.5, -0.25))
fig.savefig(FIG + "fig_8_7_bar_stacked.png", dpi=200)
plt.close(fig)
print(share.round(1))
