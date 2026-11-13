"""Chapter 1 figures (300 DPI) in DevDash brand palette."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

for f in list(Path("/usr/share/fonts/opentype/inter").glob("Inter-*.otf")) + list(Path.home().joinpath(".fonts").glob("*.ttf")):
    fm.fontManager.addfont(str(f))
NAVY, TEAL, GOLD = "#1B2A41", "#0E9AA7", "#C9A227"
TEAL_T, GOLD_T, GREY = "#E6F4F5", "#FAF3DE", "#4B5563"
plt.rcParams.update({"font.family": "Inter", "font.size": 10})
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def box(ax, x, y, w, h, fc, ec, lw=1.6, r=0.04):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0.01,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=2))


def arrow(ax, p, q, color=NAVY, rad=0.0, lw=1.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", zorder=1, shrinkA=2, shrinkB=2))


def lifecycle():
    import numpy as np
    phases = [
        ("Ask", "Has the 90-day repeat rate\nfor new customers fallen\nsince 2023?"),
        ("Prepare", "Locate orders: customer,\ndate and status, 2023–2025.\nCheck coverage and access."),
        ("Process", "Drop cancelled orders,\nfix types, find each\ncustomer's first order."),
        ("Analyse", "Did a second order follow\nwithin 90 days? Compare\nrates by quarter."),
        ("Share", "One headline, one chart,\nthe caveats and a\nrecommendation."),
        ("Act", "Decide where to invest,\nthen monitor the rate\neach quarter."),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    ax.set_xlim(-5.2, 5.2); ax.set_ylim(-4.15, 4.15); ax.axis("off"); ax.set_aspect("equal")
    R = 3.05
    angles = [90 - i * 60 for i in range(6)]
    pts = [(R * np.cos(np.radians(a)), R * np.sin(np.radians(a))) for a in angles]
    ax.add_patch(plt.Circle((0, 0), R, fill=False, ec="#D5DBE3", lw=10, zorder=0))
    for i in range(6):
        a0, a1 = np.radians(angles[i] - 17), np.radians(angles[(i + 1) % 6] + 17)
        p = (R * np.cos(a0), R * np.sin(a0)); q = (R * np.cos(a1), R * np.sin(a1))
        arrow(ax, p, q, color=TEAL, rad=-0.18, lw=2.2)
    for i, ((name, ex), (x, y)) in enumerate(zip(phases, pts)):
        box(ax, x, y, 2.75, 1.55, "white", NAVY if i else GOLD, lw=2)
        ax.text(x - 1.22, y + 0.5, f"{i + 1}", color=GOLD, fontsize=13, fontweight="bold", fontfamily="Playfair Display", va="center")
        ax.text(x, y + 0.5, name, color=NAVY, fontsize=13, fontweight="bold", ha="center", va="center", fontfamily="Playfair Display")
        ax.text(x, y - 0.2, ex, color=GREY, fontsize=7.6, ha="center", va="center", linespacing=1.35)
    ax.text(0, 0.28, "The analytics", ha="center", va="center", fontsize=15, color=NAVY, fontfamily="Playfair Display", fontweight="bold")
    ax.text(0, -0.22, "lifecycle", ha="center", va="center", fontsize=15, color=NAVY, fontfamily="Playfair Display", fontweight="bold")
    ax.text(0, -0.72, "Act raises new questions:\nthe loop begins again", ha="center", va="center", fontsize=7.8, color=TEAL, style="italic")
    fig.savefig(OUT / "fig_1_1_lifecycle.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def decision_tree():
    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    Q = lambda x, y, t: (box(ax, x, y, 2.9, 0.82, TEAL_T, TEAL, r=0.08), ax.text(x, y, t, ha="center", va="center", fontsize=8.6, color=NAVY, linespacing=1.3))
    def A(x, y, title, ex):
        box(ax, x, y, 2.05, 1.05, NAVY, NAVY, r=0.06)
        ax.text(x, y + 0.2, title, ha="center", va="center", fontsize=11, color="white", fontweight="bold", fontfamily="Playfair Display")
        ax.text(x, y - 0.24, ex, ha="center", va="center", fontsize=7, color="#E5E9F0", linespacing=1.25)
    def lab(x, y, t):
        ax.text(x, y, t, ha="center", va="center", fontsize=8, color=GOLD, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"), zorder=3)
    Q(5, 6.4, "Would adding or averaging\nthe values mean anything?")
    Q(2.4, 4.75, "Do the categories have\na natural order?")
    Q(7.6, 4.75, "Does zero mean\n\"none of this quantity\"?")
    A(1.15, 2.6, "Nominal", "province, payment\nmethod, customer_id")
    A(3.65, 2.6, "Ordinal", "loyalty_tier,\nsatisfaction_rating")
    A(6.35, 2.6, "Interval", "birth_year,\ntemperature in °C")
    A(8.85, 2.6, "Ratio", "total_spend_zmw,\nage, weight_kg")
    arrow(ax, (4.3, 6.1), (2.9, 5.18)); lab(3.35, 5.75, "No")
    arrow(ax, (5.7, 6.1), (7.1, 5.18)); lab(6.65, 5.75, "Yes")
    arrow(ax, (1.9, 4.33), (1.3, 3.15)); lab(1.45, 3.85, "No")
    arrow(ax, (2.9, 4.33), (3.5, 3.15)); lab(3.35, 3.85, "Yes")
    arrow(ax, (7.1, 4.33), (6.5, 3.15)); lab(6.65, 3.85, "No")
    arrow(ax, (8.1, 4.33), (8.7, 3.15)); lab(8.55, 3.85, "Yes")
    ax.add_patch(FancyBboxPatch((0.1, 0.35), 4.6, 1.15, boxstyle="round,pad=0.02,rounding_size=0.06", fc=GOLD_T, ec=GOLD, lw=1.2))
    ax.text(2.4, 1.18, "QUALITATIVE (categorical)", ha="center", fontsize=8.5, color="#8A6D0F", fontweight="bold")
    ax.text(2.4, 0.72, "Summarise with counts and proportions;\nmedian and percentiles if ordinal", ha="center", va="center", fontsize=7.6, color=GREY)
    ax.add_patch(FancyBboxPatch((5.3, 0.35), 4.6, 1.15, boxstyle="round,pad=0.02,rounding_size=0.06", fc=GOLD_T, ec=GOLD, lw=1.2))
    ax.text(7.6, 1.18, "QUANTITATIVE (numeric)", ha="center", fontsize=8.5, color="#8A6D0F", fontweight="bold")
    ax.text(7.6, 0.72, "Then ask: countable steps (discrete)\nor any value in a range (continuous)?", ha="center", va="center", fontsize=7.6, color=GREY)
    fig.savefig(OUT / "fig_1_2_decision_tree.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    lifecycle()
    decision_tree()
    print("figures written to", OUT)
