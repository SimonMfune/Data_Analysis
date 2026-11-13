"""Figure 13.1: training and serving in Price Advisor. Run from the repository root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.style.use("shared/kb.mplstyle")
NAVY, TEAL, GOLD, GREY, CORAL = "#1B2A41", "#0E9AA7", "#A8841A", "#4A5561", "#C8553D"
fig, ax = plt.subplots(figsize=(10.5, 5.4))
ax.set_xlim(0, 105)
ax.set_ylim(0, 60)
ax.axis("off")


def box(x, y, w, h, title, lines, colour, fill="white", mono=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                facecolor=fill, edgecolor=colour, linewidth=1.4))
    ax.text(x + w / 2, y + h - 2.4, title, ha="center", va="top", fontsize=10, fontweight="bold",
            color=NAVY, family="monospace" if mono else None)
    ax.text(x + w / 2, y + h - 6.4, "\n".join(lines), ha="center", va="top", fontsize=8, color=GREY,
            linespacing=1.4)


def arrow(a, b, label=None, dy=1.2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color=GREY, lw=1.1))
    if label:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy, label, ha="center", fontsize=7.8,
                color=GREY, style="italic")


ax.text(1, 57.5, "TRAINING  (run when data or the model changes)", fontsize=9, fontweight="bold", color=GOLD)
ax.text(1, 27.5, "SERVING  (every time someone uses the app)", fontsize=9, fontweight="bold", color=TEAL)
ax.plot([0, 105], [30.5, 30.5], color="#D5DBE1", linewidth=1, linestyle="--")
box(1, 36, 19, 18, "pricing CSV", ["600 products", "data/clean/"], GOLD, "#FBF5E6")
box(27, 36, 22, 18, "train.py", ["split, cross-validate", "interval quantiles", "test metrics", "refit on all data"], GOLD, "#FBF5E6")
box(56, 36, 25, 18, "price_model.joblib", ["model + interval", "metrics, effects", "test predictions", "versions, date"], NAVY, "#EEF1F5")
arrow((20.8, 45), (26.2, 45))
arrow((49.8, 45), (55.2, 45), "save")
box(1, 2, 21, 22, "views/", ["suggest", "what_if", "model_card", "batch"], TEAL)
box(29, 2, 24, 22, "serving.py", ["load_artefact", "  (cached once)", "suggest():", "price, range, margin"], TEAL)
box(60, 2, 20, 22, "guardrails.py", ["1  ≥ cost + 10%", "2  .00 .50 .99", "(3 error shown", "  in every view)"], CORAL)
box(86, 2, 18, 22, "validation.py", ["checks batch files", "before scoring:", "columns, types,", "ranges, categories"], TEAL)
arrow((68.5, 35.2), (45, 24.8))
ax.text(50, 31.8, "load only, never train", fontsize=7.8, color=GREY, style="italic", ha="right")
arrow((22.8, 13), (28.2, 13))
arrow((53.8, 13), (59.2, 13))
ax.text(95, 26.5, "app.py: page setup and navigation", ha="center", fontsize=8, color=NAVY)
fig.savefig("chapters/ch13/figures/fig_13_1_architecture.png", dpi=200)
print("wrote fig_13_1_architecture.png")
