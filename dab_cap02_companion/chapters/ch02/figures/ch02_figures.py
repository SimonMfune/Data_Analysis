"""Chapter 2 figures (300 DPI) in DevDash brand palette."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

for f in list(Path("/usr/share/fonts/opentype/inter").glob("Inter-*.otf")) + list(Path.home().joinpath(".fonts").glob("*.ttf")):
    fm.fontManager.addfont(str(f))
NAVY, TEAL, GOLD = "#1B2A41", "#0E9AA7", "#C9A227"
TEAL_T, GOLD_T, NAVY_T, GREY = "#E6F4F5", "#FAF3DE", "#E8ECF2", "#4B5563"
plt.rcParams.update({"font.family": "Inter", "font.size": 10})
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def rbox(ax, x, y, w, h, fc, ec, lw=1.4, r=0.05, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, p, q, color=NAVY, lw=1.6, rad=0.0, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=13, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", zorder=1, shrinkA=1, shrinkB=1))


def stack():
    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    cols = [
        ("Sources", "Where data is created", ["Website, app &\nWhatsApp orders", "Mobile-money &\ncard payments", "Courier tracking", "Reviews &\nsurveys"]),
        ("Storage", "Where data is kept", ["Spreadsheets\n(Excel, Sheets)", "SQL databases\n(SQLite, PostgreSQL)", "Files\n(CSV, JSON)"]),
        ("Analysis", "Where data is processed", ["Excel formulas\n& PivotTables", "SQL queries", "Python: pandas,\nNumPy, scikit-learn"]),
        ("Presentation", "Where people use the results", ["Charts &\nreports", "BI dashboards\n(Power BI, Looker)", "Streamlit apps"]),
    ]
    xs = [0.15, 2.65, 5.15, 7.65]
    w = 2.15
    for (title, sub, items), x in zip(cols, xs):
        rbox(ax, x, 1.2, w, 4.55, NAVY_T if title != "Analysis" else TEAL_T, NAVY if title != "Analysis" else TEAL, lw=1.2, r=0.08, z=0)
        ax.text(x + w / 2, 5.45, title, ha="center", fontsize=12.5, fontweight="bold", color=NAVY, fontfamily="Playfair Display")
        ax.text(x + w / 2, 5.13, sub, ha="center", fontsize=7.4, color=GREY, style="italic")
        n = len(items)
        top, bottom = 4.85, 1.4
        h = (top - bottom - 0.12 * (n - 1)) / n
        for i, it in enumerate(items):
            y = top - (i + 1) * h - i * 0.12
            rbox(ax, x + 0.15, y, w - 0.3, h, "white", NAVY, lw=1.0, r=0.06)
            ax.text(x + w / 2, y + h / 2, it, ha="center", va="center", fontsize=7.9, color=NAVY, linespacing=1.25)
    for i in range(3):
        arrow(ax, (xs[i] + w + 0.02, 3.3), (xs[i + 1] - 0.02, 3.3), color=GOLD, lw=2.4)
    rbox(ax, 0.15, 0.2, 9.65, 0.75, GOLD_T, GOLD, lw=1.2, r=0.08)
    ax.text(4.97, 0.575, "AI assistants work across every layer: drafting SQL and Python, explaining errors, summarising text, suggesting charts",
            ha="center", va="center", fontsize=8.3, color="#5C4A0B")
    fig.savefig(OUT / "fig_2_1_data_stack.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def vscode():
    fig, ax = plt.subplots(figsize=(9.4, 5.9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.3); ax.axis("off")
    dark, side, ed, term = "#1F1F1F", "#252526", "#1E1E1E", "#181818"
    ax.add_patch(Rectangle((0, 0.3), 10, 5.7, fc=dark, ec="#3C3C3C", lw=1.5))
    ax.add_patch(Rectangle((0, 5.7), 10, 0.3, fc="#2D2D2D", ec="none"))
    ax.text(5, 5.85, "first_look.py — dab-companion — Visual Studio Code", ha="center", va="center", fontsize=7.5, color="#CCCCCC")
    ax.add_patch(Rectangle((0, 0.55), 0.45, 5.15, fc="#2C2C2C", ec="none"))
    for i, y in enumerate([5.35, 4.95, 4.55, 4.15, 3.75]):
        ax.add_patch(Rectangle((0.12, y - 0.1), 0.21, 0.2, fc="#858585" if i else "#E0E0E0", ec="none"))
    ax.add_patch(Rectangle((0.45, 0.55), 2.15, 5.15, fc=side, ec="none"))
    ax.text(0.6, 5.5, "EXPLORER", fontsize=6.5, color="#BBBBBB", fontweight="bold")
    tree = ["▾ DAB-COMPANION", "  ▸ chapters", "      ▾ ch02", "        ▾ listings", "            first_look.py", "  ▸ data", "    environment.yml", "    README.md", "    requirements.txt"]
    for i, t in enumerate(tree):
        ax.text(0.58, 5.15 - i * 0.27, t, fontsize=6.6, color="#E0E0E0" if "first_look" in t else "#C5C5C5", family="Fira Code",
                bbox=dict(fc="#37373D", ec="none", pad=1.2) if "first_look" in t else None)
    ax.add_patch(Rectangle((2.6, 2.3), 7.4, 3.4, fc=ed, ec="none"))
    ax.add_patch(Rectangle((2.6, 5.4), 1.6, 0.3, fc=ed, ec="none"))
    ax.text(2.7, 5.55, "first_look.py", fontsize=6.6, color="#FFFFFF", family="Fira Code", va="center")
    code = [("# %% Load the data", "#6A9955"), ("import pandas as pd", "#C586C0"), ("", "#D4D4D4"),
            ('orders = pd.read_csv("data/clean/orders.csv",', "#D4D4D4"), ('                     parse_dates=["order_datetime"])', "#D4D4D4"),
            ("", "#D4D4D4"), ("# %% Summarise it", "#6A9955"), ('print(f"Orders: {len(orders):,}")', "#DCDCAA")]
    for i, (t, c) in enumerate(code):
        ax.text(2.75, 5.15 - i * 0.3, f"{i + 1:>2}", fontsize=6.4, color="#6E7681", family="Fira Code")
        ax.text(3.05, 5.15 - i * 0.3, t, fontsize=6.6, color=c, family="Fira Code")
    ax.add_patch(Rectangle((2.6, 0.55), 7.4, 1.75, fc=term, ec="#3C3C3C", lw=0.8))
    ax.text(2.75, 2.12, "PROBLEMS   OUTPUT   TERMINAL", fontsize=6.3, color="#BBBBBB")
    ax.plot([5.05, 5.75], [2.03, 2.03], color="#E7E7E7", lw=1)
    term_lines = ["(dab) $ python chapters/ch02/listings/first_look.py", "Orders: 62,059", "From 01 January 2023 to 31 December 2025"]
    for i, t in enumerate(term_lines):
        ax.text(2.75, 1.75 - i * 0.28, t, fontsize=6.6, color="#CCCCCC" if i else "#89D185", family="Fira Code")
    ax.add_patch(Rectangle((0, 0.3), 10, 0.25, fc="#007ACC", ec="none"))
    ax.text(0.15, 0.425, "⎇ main", fontsize=6.4, color="white", va="center")
    ax.text(7.2, 0.425, "Python   3.12.3 ('dab')", fontsize=6.4, color="white", va="center")

    def call(n, xy, txt, xyt):
        ax.annotate("", xy=xy, xytext=xyt, arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.4))
        ax.add_patch(plt.Circle(xyt, 0.17, fc=GOLD, ec="white", lw=1.2, zorder=5))
        ax.text(*xyt, str(n), ha="center", va="center", fontsize=8, fontweight="bold", color=NAVY, zorder=6)
    call(1, (0.22, 5.35), "", (0.22, 6.2) if False else (-0.25, 5.35))
    call(2, (1.5, 2.6), "", (1.5, 1.2))
    call(3, (6.0, 4.0), "", (9.5, 4.6))
    call(4, (6.0, 1.2), "", (9.5, 1.5))
    call(5, (8.0, 0.42), "", (8.4, -0.05))
    call(6, (0.5, 0.42), "", (0.9, -0.05))
    ax.set_xlim(-0.55, 10.1); ax.set_ylim(-0.3, 6.1)
    fig.savefig(OUT / "fig_2_2_vscode.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def git():
    fig, ax = plt.subplots(figsize=(9.4, 3.9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.1); ax.axis("off")
    zones = [(0.1, "Working folder", "Files you edit\nin VS Code", NAVY_T, NAVY),
             (2.6, "Staging area", "Changes chosen\nfor the next commit", NAVY_T, NAVY),
             (5.1, "Local repository", "Saved snapshots\n(commits) on your PC", TEAL_T, TEAL),
             (7.6, "GitHub (remote)", "A copy online:\nbackup and portfolio", GOLD_T, GOLD)]
    for x, t, s, fc, ec in zones:
        rbox(ax, x, 1.55, 2.3, 1.7, fc, ec, lw=1.6, r=0.08)
        ax.text(x + 1.15, 2.85, t, ha="center", fontsize=11.5, fontweight="bold", color=NAVY, fontfamily="Playfair Display")
        ax.text(x + 1.15, 2.15, s, ha="center", va="center", fontsize=8.2, color=GREY, linespacing=1.3)
    for (x0, x1, lab) in [(2.4, 2.6, "git add"), (4.9, 5.1, "git commit"), (7.4, 7.6, "git push")]:
        arrow(ax, (x0, 2.65), (x1, 2.65), color=GOLD, lw=2.4)
        ax.text((x0 + x1) / 2, 3.6, lab, ha="center", fontsize=9, family="Fira Code", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GOLD, lw=1))
        ax.plot([(x0 + x1) / 2] * 2, [3.42, 2.75], color=GOLD, lw=1)
    ax.plot([8.75, 8.75, 1.25], [1.55, 0.95, 0.95], color=TEAL, lw=1.8, zorder=1)
    arrow(ax, (1.25, 0.95), (1.25, 1.55), color=TEAL, lw=1.8)
    ax.text(5.0, 0.5, "git clone / git pull  —  bring a repository (or its latest changes) from GitHub to your computer",
            ha="center", fontsize=8.4, color=TEAL)
    fig.savefig(OUT / "fig_2_3_git_workflow.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    stack(); vscode(); git()
    print("figures written to", OUT)
