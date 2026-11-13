"""Figure 11.1: the machine-learning workflow. Run from the repository root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.style.use("shared/kb.mplstyle")
NAVY, TEAL, GOLD, GREY = "#1B2A41", "#0E9AA7", "#A8841A", "#4A5561"
steps = [("1  Frame", "What to predict,\nfor whom, and how\nit will be used"),
         ("2  Prepare", "Clean data, choose\nfeatures, split train\nand test (11.3)"),
         ("3  Train", "Fit a pipeline on the\ntraining set only\n(11.4-11.6)"),
         ("4  Evaluate", "Metrics, residuals,\ncross-validation\n(11.7, 11.9)"),
         ("5  Interpret", "Coefficients and\nassumptions\n(11.8)"),
         ("6  Deploy", "Save, reload, predict,\nmonitor (11.10)")]
fig, ax = plt.subplots(figsize=(10.5, 3.6))
ax.set_xlim(0, 109)
ax.set_ylim(-3, 36)
ax.axis("off")
w, gap = 15, 3
for i, (title, text) in enumerate(steps):
    x = 1 + i * (w + gap)
    colour = GOLD if i in (0, 5) else TEAL
    ax.add_patch(FancyBboxPatch((x, 9), w, 20, boxstyle="round,pad=0.3,rounding_size=1.2",
                                facecolor="white", edgecolor=colour, linewidth=1.5))
    ax.text(x + w / 2, 25.5, title, ha="center", fontsize=10, fontweight="bold", color=NAVY)
    ax.text(x + w / 2, 21.5, text, ha="center", va="top", fontsize=8, color=GREY, linespacing=1.4)
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.3, 19), (x + w + gap - 0.3, 19), arrowstyle="-|>",
                                     mutation_scale=11, color=GREY))
ax.add_patch(FancyArrowPatch((80, 8.5), (28, 8.5), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>",
                             mutation_scale=11, color=GREY, linestyle="--"))
ax.text(54, -2.5, "not good enough? return to features or model; the test set is used once, at the end",
        ha="center", fontsize=8.3, color=GREY, style="italic")
fig.savefig("chapters/ch11/figures/fig_11_1_workflow.png", dpi=200)
print("wrote fig_11_1_workflow.png")
