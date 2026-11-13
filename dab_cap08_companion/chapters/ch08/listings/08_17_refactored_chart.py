# One production-grade answer: sorted bars, one highlight colour, direct labels
share = cat2025.sort_values() / cat2025.sum() * 100
colours = ["#0E9AA7" if name == "Electronics" else "#B8C2CC" for name in share.index]

fig, ax = plt.subplots(figsize=(8, 3.8))
bars = ax.barh(share.index, share.values, color=colours, height=0.7)
ax.bar_label(bars, labels=[f"{v:.0f}%  ({kwacha(r)})" for v, r in
                           zip(share, cat2025[share.index])], padding=4, fontsize=9)
ax.set_title("Electronics earned a third of 2025 revenue; no other category reached 14%")
ax.set_xlabel("Share of 2025 revenue (%)")
ax.grid(axis="y", visible=False)
ax.grid(axis="x", visible=True)
ax.margins(x=0.25)
fig.savefig(FIG + "fig_8_16_refactored.png", dpi=200)
plt.close(fig)
print(share.sort_values(ascending=False).round(1).to_string())
