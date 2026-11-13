"""Figure 10.1: probability tree for the fraud flag. Run from the repository root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use("shared/kb.mplstyle")
NAVY, TEAL, CORAL, GREY = "#1B2A41", "#0E9AA7", "#C8553D", "#4A5561"
fig, ax = plt.subplots(figsize=(9.5, 5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.axis("off")


def node(x, y, text, colour=NAVY, bold=False):
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5, color=colour,
            fontweight="bold" if bold else "normal",
            bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": colour, "lw": 1.1})


def edge(x0, y0, x1, y1, label):
    ax.plot([x0, x1], [y0, y1], color=GREY, lw=1)
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 1.6, label, ha="center", fontsize=8.5, color=GREY, style="italic")


node(8, 30, "10,000\ndigital\npayments", bold=True)
edge(13, 32, 33, 46, "fraud 0.5%")
edge(13, 28, 33, 14, "genuine 99.5%")
node(40, 46, "50 fraudulent", CORAL)
node(40, 14, "9,950 genuine", TEAL)
edge(48, 47, 66, 55, "flagged 90%")
edge(48, 45, 66, 38, "missed 10%")
edge(48, 15, 66, 22, "flagged 3%")
edge(48, 13, 66, 5, "cleared 97%")
node(76, 55, "45 fraud, flagged", CORAL, True)
node(76, 38, "5 fraud, missed", CORAL)
node(76, 22, "about 299 genuine, flagged", TEAL, True)
node(76, 5, "9,652 genuine, cleared", TEAL)
ax.text(1, 3, "Flagged: 45 + 299 = 344\nFraud among flagged: 45 / 344 = 13%",
        ha="left", va="bottom", fontsize=10, color=NAVY, fontweight="bold")
fig.savefig("chapters/ch10/figures/fig_10_1_bayes_tree.png", dpi=200)
print("wrote fig_10_1_bayes_tree.png")
