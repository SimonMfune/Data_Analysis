"""Chapter 6 figures: missing-value matrix (6.1) and the cleaning pipeline (6.2).

Run from the repository root:  python chapters/ch06/figures/ch06_figures.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

for f in list(Path("/usr/share/fonts/opentype/inter").glob("Inter-*.otf")) + list(Path.home().joinpath(".fonts").glob("*.ttf")):
    fm.fontManager.addfont(str(f))
NAVY, TEAL, GOLD, GREY = "#1B2A41", "#0E9AA7", "#C9A227", "#4B5563"
TEAL_T, GOLD_T, NAVY_T = "#E6F4F5", "#FAF3DE", "#E8ECF2"
plt.rcParams.update({"font.family": "Inter", "font.size": 9})
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent


def missing_matrix():
    m = pd.read_csv(ROOT / "data/raw/kb_orders_messy.csv")
    miss = m.isna()
    fig = plt.figure(figsize=(9.4, 4.6))
    ax = fig.add_axes([0.06, 0.12, 0.66, 0.74])
    img = np.where(miss.values, 1.0, 0.0)
    ax.imshow(img.T, aspect="auto", interpolation="nearest", cmap=matplotlib.colors.ListedColormap([TEAL_T, GOLD]))
    ax.set_yticks(range(len(m.columns))); ax.set_yticklabels(m.columns, family="Fira Code", fontsize=7.6)
    ax.set_xlabel(f"Row number (all {len(m):,} rows of kb_orders_messy.csv)", fontsize=8, color=GREY)
    ax.set_title("Missing values (gold) by column and row", loc="left", fontsize=10.5, color=NAVY, fontweight="bold")
    ax.tick_params(axis="x", labelsize=7.5, colors=GREY)
    for s in ax.spines.values():
        s.set_visible(False)
    bx = fig.add_axes([0.76, 0.12, 0.21, 0.74])
    counts = miss.sum().values
    bx.barh(range(len(m.columns)), counts, color=[GOLD if c else "#D5DBE3" for c in counts])
    bx.set_ylim(len(m.columns) - 0.5, -0.5); bx.set_yticks([])
    for i, c in enumerate(counts):
        if c:
            bx.text(c + 5, i, f"{c}", va="center", fontsize=7.6, color=NAVY)
    bx.set_title("Count", loc="left", fontsize=9, color=NAVY, fontweight="bold")
    bx.set_xlim(0, counts.max() * 1.35)
    bx.tick_params(labelsize=7, colors=GREY)
    for s in ("top", "right"):
        bx.spines[s].set_visible(False)
    fig.savefig(OUT / "fig_6_1_missing_matrix.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def pipeline():
    steps = [("Load as text", "dtype=str\nkeep 'None'"), ("Strip spaces", "all text\ncolumns"), ("Drop exact\nduplicates", "151 rows"),
             ("Standardise\ncategories", "channel,\nprovince"), ("Drop repeated\norder IDs", "39 rows"),
             ("Parse dates", "3 explicit\nformats"), ("Parse money\n& phones", "K1,541.48 ->\n1541.48"),
             ("Fix by rule", "negatives,\nx100 subtotals"), ("Fill missing", "derive, borrow\nor 'Unknown'"),
             ("Validate", "assert every\nrule")]
    fig, ax = plt.subplots(figsize=(9.4, 3.3))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.4); ax.axis("off")
    w, h = 1.72, 1.05
    pos = [(0.1 + (i % 5) * 1.98, 2.15 if i < 5 else 0.55) for i in range(10)]
    for i, ((t, s), (x, y)) in enumerate(zip(steps, pos)):
        fc, ec = (GOLD_T, GOLD) if i == 9 else (TEAL_T, TEAL) if i in (5, 6) else (NAVY_T, NAVY)
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06", fc=fc, ec=ec, lw=1.3))
        ax.text(x + 0.12, y + h - 0.2, str(i + 1), fontsize=9, color=GOLD, fontweight="bold", fontfamily="Playfair Display")
        ax.text(x + w / 2, y + h * 0.66, t, ha="center", va="center", fontsize=8.2, fontweight="bold", color=NAVY, linespacing=1.15)
        ax.text(x + w / 2, y + h * 0.24, s, ha="center", va="center", fontsize=6.9, color=GREY, linespacing=1.15)
        if i not in (4, 9):
            ax.add_patch(FancyArrowPatch((x + w + 0.02, y + h / 2), (x + 1.96, y + h / 2), arrowstyle="-|>", mutation_scale=11, color=GOLD, lw=1.6))
    x5, x6 = pos[4][0] + w / 2, pos[5][0] + w / 2
    ax.plot([x5, x5, x6], [2.13, 1.86, 1.86], color=GOLD, lw=1.6)
    ax.add_patch(FancyArrowPatch((x6, 1.86), (x6, 1.62), arrowstyle="-|>", mutation_scale=11, color=GOLD, lw=1.6))
    ax.text(5, 3.3, "Each step is a function: DataFrame in, DataFrame out, one line added to the cleaning log",
            ha="center", fontsize=8.4, color=NAVY, style="italic")
    fig.savefig(OUT / "fig_6_2_pipeline.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    missing_matrix(); pipeline()
    print("figures written")
