"""Non-listing figures for Chapter 8: anatomy of a figure (8.1) and the palette check (8.14).
Run from the repository root: python chapters/ch08/figures/ch08_figures.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use("shared/kb.mplstyle")
FIG = "chapters/ch08/figures/"
k = pd.read_csv("data/clean/kb_monthly_kpis.csv")
k["month"] = pd.to_datetime(k["month"], format="%Y-%m")
m = k.groupby("month")["revenue_zmw"].sum() / 1e6
m24, m25 = m.loc["2024"], m.loc["2025"]

# ---- Figure 8.1: anatomy -------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.6))
fig.patch.set_facecolor("#F4F6F8")
x = np.arange(1, 13)
ax.plot(x, m24.values, marker="o", label="2024")
ax.plot(x, m25.values, marker="o", label="2025")
ax.set_xticks(x, ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
ax.set_title("Monthly revenue, 2024 and 2025")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (K million)")
ax.set_ylim(0, 5.2)
ax.legend(loc="upper left")
note = dict(fontsize=8.5, color="#C8553D", fontweight="bold", annotation_clip=False,
            arrowprops=dict(arrowstyle="->", color="#C8553D", lw=1, shrinkA=2, shrinkB=2))
ax.annotate("Title  ax.set_title()", xy=(0.41, 1.065), xycoords="axes fraction",
            xytext=(0.62, 0.95), textcoords="figure fraction", **note)
ax.annotate("Legend  ax.legend()", xy=(0.14, 0.86), xycoords="axes fraction", xytext=(3.4, 4.3), textcoords="data", **note)
ax.annotate("y-axis label  ax.set_ylabel()", xy=(-0.075, 0.62), xycoords="axes fraction",
            xytext=(1.0, 3.3), textcoords="data", **note)
ax.annotate("Line  ax.plot()", xy=(10, m25.iloc[9]), xytext=(6.6, 3.7), **note)
ax.annotate("Grid line", xy=(5.6, 1.0), xytext=(6.2, 0.4), **note)
ax.annotate("Spine", xy=(11.6, 0), xytext=(10.6, 0.7), **note)
ax.annotate("Major tick label", xy=(0.955, -0.06), xycoords="axes fraction",
            xytext=(0.80, 0.035), textcoords="figure fraction", **note)
fig.text(0.985, 0.93, "Figure: the whole canvas (grey)\nAxes: the plotting area (white)",
         ha="right", va="top", fontsize=8.5, color="#C8553D", fontweight="bold")
fig.savefig(FIG + "fig_8_1_anatomy.png", dpi=200)
plt.close(fig)

# ---- Figure 8.14: palette under normal vision, deuteranopia and greyscale ------
palette = ["#0E9AA7", "#A8841A", "#2F5D9E", "#C8553D", "#6B4E9B", "#5E8C31"]
names = ["Teal", "Gold", "Blue", "Coral", "Purple", "Green"]
rgb = np.array([matplotlib.colors.to_rgb(c) for c in palette])
lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
deut = np.array([[0.367322, 0.860646, -0.227968],      # Machado et al. (2009),
                 [0.280085, 0.672501, 0.047413],       # deuteranopia, severity 1.0
                 [-0.011820, 0.042940, 0.968881]])
sim = np.clip(lin @ deut.T, 0, 1)
to_srgb = lambda a: np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)
grey = (lin @ np.array([0.2126, 0.7152, 0.0722]))[:, None].repeat(3, axis=1)
rows = [("Normal vision", rgb), ("Deuteranopia (simulated)", to_srgb(sim)), ("Greyscale", to_srgb(grey))]

fig, ax = plt.subplots(figsize=(8, 3.0))
for r, (label, colours) in enumerate(rows):
    for c, colour in enumerate(colours):
        ax.add_patch(plt.Rectangle((c + 0.05, -r - 0.9), 0.9, 0.8, color=colour))
    ax.text(-0.1, -r - 0.5, label, ha="right", va="center", fontsize=9)
for c, (n, h) in enumerate(zip(names, palette)):
    ax.text(c + 0.5, 0.15, f"{n}\n{h}", ha="center", va="bottom", fontsize=8)
ax.set_xlim(-2.6, 6.1)
ax.set_ylim(-3.1, 0.8)
ax.axis("off")
fig.savefig(FIG + "fig_8_14_palette.png", dpi=200)
plt.close(fig)
print("wrote fig_8_1_anatomy.png and fig_8_14_palette.png")
