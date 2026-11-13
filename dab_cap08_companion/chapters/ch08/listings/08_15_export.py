from pathlib import Path

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(monthly.index, monthly["revenue_zmw"])
ax.yaxis.set_major_formatter(FuncFormatter(kwacha))
ax.set_title("Monthly revenue")

out = Path("chapters/ch08/outputs/export")
out.mkdir(exist_ok=True)
fig.savefig(out / "revenue_web.png", dpi=100)        # screens and slides
fig.savefig(out / "revenue_print.png", dpi=300)      # print
fig.savefig(out / "revenue.svg")                     # vector: scales without blurring
fig.savefig(out / "revenue.pdf")                     # vector, for LaTeX and print shops
plt.close(fig)
for f in sorted(out.iterdir()):
    print(f"{f.name:<18} {f.stat().st_size / 1024:6.0f} KB")
