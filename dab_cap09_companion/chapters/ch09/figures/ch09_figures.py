"""Figure 9.1: architecture of the Quick EDA app. Run from the repository root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.style.use("shared/kb.mplstyle")
NAVY, TEAL, GOLD, GREY, LIGHT = "#1B2A41", "#0E9AA7", "#A8841A", "#4A5561", "#E8F6F7"

fig, ax = plt.subplots(figsize=(10, 5.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.axis("off")


def box(x, y, w, h, title, lines, colour=TEAL, fill=LIGHT):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                facecolor=fill, edgecolor=colour, linewidth=1.4))
    ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="top", fontsize=10.5,
            fontweight="bold", color=NAVY, family="monospace" if title.endswith(".py") else None)
    ax.text(x + w / 2, y + h - 7, "\n".join(lines), ha="center", va="top", fontsize=8.3,
            color=GREY, linespacing=1.45)


def arrow(a, b, text=None, offset=(0, 1.4)):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=GREY, lw=1.1))
    if text:
        ax.text((a[0] + b[0]) / 2 + offset[0], (a[1] + b[1]) / 2 + offset[1], text,
                ha="center", fontsize=7.8, color=GREY, style="italic")


box(1, 40, 17, 15, "User", ["uploads a CSV", "or picks a sample,", "sets options"], colour=GOLD, fill="#FBF5E6")
box(30, 36, 40, 21, "app.py", ["page layout, sidebar, tabs", "widgets and session state",
                               "@st.cache_data wrappers", "calls the modules; holds no logic"], colour=NAVY, fill="#EEF1F5")
box(1, 4, 22, 22, "loader.py", ["M1", "decode (utf-8, cp1252, latin-1)", "sniff the delimiter",
                                "read as text, infer types"])
box(26, 4, 22, 22, "profiling.py", ["M2", "column roles, missing,", "distinct values, duplicates",
                                    "numeric summary"])
box(51, 4, 22, 22, "cleaning.py", ["M3", "CleaningOptions", "clean(df, options)", "returns data + change log"])
box(76, 4, 22, 22, "charts.py", ["M4", "house style (kb.mplstyle)", "histogram, bars, box,", "scatter, over time"])
box(81, 40, 17, 15, "Outputs", ["tables and charts", "cleaned CSV", "cleaning log CSV (M5)"], colour=GOLD, fill="#FBF5E6")

arrow((18.8, 47.5), (29.2, 47.5), "bytes, choices")
arrow((70.8, 47.5), (80.2, 47.5), "render")
for x in (12, 37, 62, 87):
    arrow((50 if x > 50 else 50, 35.2), (x, 26.8))
ax.text(50, 30.3, "plain functions: DataFrame in, DataFrame or figure out", ha="center",
        fontsize=8, color=GREY, style="italic",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1})
ax.text(50, 0.3, "tests/ checks each module directly and the whole app with Streamlit's AppTest",
        ha="center", fontsize=8.3, color=NAVY)
fig.savefig("chapters/ch09/figures/fig_9_1_architecture.png", dpi=200)
print("wrote fig_9_1_architecture.png")
