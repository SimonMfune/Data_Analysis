"""Chapter 3 figures (300 DPI), drawn from data/raw/kb_raw_transactions.xlsx.

Run from the repository root:  python chapters/ch03/figures/ch03_figures.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

for f in list(Path("/usr/share/fonts/opentype/inter").glob("Inter-*.otf")) + list(Path.home().joinpath(".fonts").glob("*.ttf")):
    fm.fontManager.addfont(str(f))
NAVY, TEAL, GOLD = "#1B2A41", "#0E9AA7", "#C9A227"
TEAL_T, GOLD_T, NAVY_T, GREY = "#E6F4F5", "#FAF3DE", "#E8ECF2", "#4B5563"
XL_GREEN = "#217346"
plt.rcParams.update({"font.family": "Inter", "font.size": 9})
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solutions"))
from check_results import clean  # noqa: E402

RAW_ALL, CLEAN = clean()
RAW = RAW_ALL.drop_duplicates().reset_index(drop=True)
CLEAN = CLEAN.reset_index(drop=True)
CLEAN["Customer Clean"] = CLEAN["Customer Clean"].str.replace("Ng'a", "Ng'A")  # figure re-applies the fix itself
_pv = CLEAN.pivot_table(index="Province Clean", columns="Quarter", values="Line Total", aggfunc="sum",
                        margins=True, margins_name="Grand Total").round(0)
_pv.columns = [c.replace("Qtr", "Q") for c in _pv.columns]
_pv = _pv.sort_values("Grand Total", ascending=False)
EXP = {
    "province_values": sorted(CLEAN["Province Clean"].unique()),
    "category_values": sorted(CLEAN["Category Clean"].unique()),
    "payment_values": CLEAN["Payment Clean"].value_counts().to_dict(),
    "pivot_province_quarter": _pv.to_dict(orient="index"),
    "total_revenue": CLEAN["Line Total"].sum(),
    "lines": len(CLEAN),
    "avg_line": round(CLEAN["Line Total"].mean(), 2),
    "margin_pct": round(CLEAN["Gross Margin"].sum() / CLEAN["Line Total"].sum() * 100, 1),
    "rev_by_province": CLEAN.groupby("Province Clean")["Line Total"].sum().to_dict(),
    "rev_by_month": CLEAN.groupby("Month")["Line Total"].sum().to_dict(),
    "rev_by_payment": CLEAN.groupby("Payment Clean")["Line Total"].sum().to_dict(),
}

def grid(ax, x0, y0, headers, rows, widths, flags, title, fill_flag, letters):
    rh = 0.42
    ax.text(x0, y0 + 0.62, title, fontsize=11, fontweight="bold", color=NAVY, fontfamily="Playfair Display")
    ax.add_patch(Rectangle((x0, y0 - rh * (len(rows) + 1)), 0.45, rh * (len(rows) + 1), fc="#F3F3F3", ec="#C8C8C8", lw=0.6))
    x = x0 + 0.45
    for j, (h, w) in enumerate(zip(headers, widths)):
        ax.add_patch(Rectangle((x, y0), w, 0.3, fc="#F3F3F3", ec="#C8C8C8", lw=0.6))
        ax.text(x + w / 2, y0 + 0.15, letters[j], ha="center", va="center", fontsize=7, color="#666")
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc=XL_GREEN if False else "#DDEBF7", ec="#C8C8C8", lw=0.6))
        ax.text(x + 0.08, y0 - rh / 2, h, va="center", fontsize=7.6, fontweight="bold", color=NAVY)
        for i, r in enumerate(rows):
            y = y0 - rh * (i + 2)
            flagged = flags[i][j]
            ax.add_patch(Rectangle((x, y), w, rh, fc=fill_flag if flagged else "white", ec="#C8C8C8", lw=0.6))
            v = r[j]
            ha, tx = ("right", x + w - 0.08) if isinstance(v, (int, float)) and not isinstance(v, bool) else ("left", x + 0.08)
            txt = f"{v:,.2f}" if isinstance(v, float) else str(v)
            ax.text(tx, y + rh / 2, txt, va="center", ha=ha, fontsize=7.6, color=NAVY, family="Fira Code" if flagged else "Inter")
        x += w
    for i in range(len(rows) + 1):
        ax.text(x0 + 0.225, y0 - rh * (i + 0.5), str(i + 1), ha="center", va="center", fontsize=7, color="#666")


def before_after():
    idx = [5, 12, 20, 23, 25, 54]
    raw = RAW.loc[idx]
    cl = CLEAN.loc[idx]
    vis = lambda s: s.replace(" ", "·") if (s != s.strip() or "  " in s) else s
    hdr = ["Customer Name", "Province", "Category", "Unit Price", "Payment Method"]
    rows_r, fl_r = [], []
    for _, r in raw.iterrows():
        vals = [vis(r["Customer Name"]), vis(r["Province"]), vis(r["Category"]), r["Unit Price"], r["Payment Method"]]
        flags = [r["Customer Name"] != r["Customer Name"].strip() or "  " in r["Customer Name"] or r["Customer Name"].islower(),
                 r["Province"] not in EXP["province_values"], r["Category"] not in EXP["category_values"],
                 isinstance(r["Unit Price"], str), r["Payment Method"] not in EXP["payment_values"]]
        rows_r.append(vals); fl_r.append(flags)
    cust_fix = [c.replace("Ng'Andu", "Ng'andu") for c in cl["Customer Clean"]]
    rows_c = [[cf, p, c, float(pr), pm] for cf, p, c, pr, pm in zip(cust_fix, cl["Province Clean"], cl["Category Clean"], cl["Price Clean"], cl["Payment Clean"])]
    fl_c = [[f for f in fr] for fr in fl_r]
    fig, ax = plt.subplots(figsize=(9.6, 7.0))
    ax.set_xlim(0, 10.2); ax.set_ylim(-0.9, 7.35); ax.axis("off")
    widths = [2.15, 1.45, 1.75, 1.45, 1.75]
    grid(ax, 0.2, 6.55, hdr, rows_r, widths, fl_r, "Before: as exported (Transactions sheet)", GOLD_T, list("CDGIJ"))
    grid(ax, 0.2, 2.6, ["Customer Clean", "Province Clean", "Category Clean", "Price Clean", "Payment Clean"], rows_c, widths, fl_c, "After: helper columns with cleaning formulas", TEAL_T, ["M", "K", "L", "O", "N"])
    ax.add_patch(FancyArrowPatch((5.1, 3.45), (5.1, 3.1), arrowstyle="-|>", mutation_scale=16, color=GOLD, lw=2))
    ax.text(0.2, -0.75, "Highlighted cells contain a defect (before) and the corrected value (after). · marks a space. Rows are real lines from kb_raw_transactions.xlsx.",
            fontsize=7.4, color=GREY, style="italic")
    fig.savefig(OUT / "fig_3_1_before_after.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def pivot_layout():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.8); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.1, 0.25), 3.7, 4.35, boxstyle="round,pad=0,rounding_size=0.06", fc="#FAFAFA", ec="#BDBDBD"))
    ax.text(0.3, 4.3, "PivotTable Fields", fontsize=10, fontweight="bold", color=NAVY)
    fields = ["Date", "Province Clean", "Category Clean", "Payment Clean", "Line Total", "Gross Margin"]
    for i, f in enumerate(fields):
        y = 3.95 - i * 0.27
        ax.add_patch(Rectangle((0.32, y - 0.08), 0.13, 0.13, fc=TEAL if f in ("Date", "Province Clean", "Line Total") else "white", ec="#888", lw=0.7))
        ax.text(0.55, y - 0.02, f, fontsize=7.8, color=NAVY, va="center")
    areas = [("Filters", "(Category Clean)", 0.3, 1.95), ("Columns", "Quarters (from Date)", 2.05, 1.95), ("Rows", "Province Clean", 0.3, 0.95), ("Values", "Sum of Line Total", 2.05, 0.95)]
    for name, val, x, y in areas:
        ax.add_patch(Rectangle((x, y - 0.55), 1.6, 0.85, fc="white", ec="#BDBDBD"))
        ax.text(x + 0.08, y + 0.15, name, fontsize=7.6, fontweight="bold", color=GREY)
        ax.add_patch(FancyBboxPatch((x + 0.1, y - 0.42), 1.4, 0.3, boxstyle="round,pad=0,rounding_size=0.04", fc=TEAL_T if "(" not in val else "#F5F5F5", ec=TEAL if "(" not in val else "#BDBDBD", lw=0.8))
        ax.text(x + 0.8, y - 0.27, val, fontsize=6.9, ha="center", va="center", color=NAVY)
    ax.add_patch(FancyArrowPatch((3.9, 2.4), (4.45, 2.4), arrowstyle="-|>", mutation_scale=16, color=GOLD, lw=2.2))
    pv = EXP["pivot_province_quarter"]
    order = [k for k in pv if k != "Grand Total"][:5]
    cols = ["Q1", "Q2", "Q3", "Q4", "Grand Total"]
    x0, y0, rh = 4.6, 4.35, 0.36
    cw = [1.4] + [0.78] * 4 + [0.95]
    hdrs = ["Sum of Line Total", "Qtr1", "Qtr2", "Qtr3", "Qtr4", "Grand Total"]
    x = x0
    for w, h in zip(cw, hdrs):
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#DDEBF7", ec="#C8C8C8", lw=0.6))
        ax.text(x + w - 0.06 if h != hdrs[0] else x + 0.06, y0 - rh / 2, h, fontsize=6.9, fontweight="bold", color=NAVY, va="center", ha="right" if h != hdrs[0] else "left")
        x += w
    rows = order + ["…", "Grand Total"]
    for i, r in enumerate(rows):
        y = y0 - rh * (i + 2); x = x0
        bold = r == "Grand Total"
        for j, w in enumerate(cw):
            ax.add_patch(Rectangle((x, y), w, rh, fc="#DDEBF7" if bold else "white", ec="#C8C8C8", lw=0.6))
            if j == 0:
                ax.text(x + 0.06, y + rh / 2, r, fontsize=7, va="center", color=NAVY, fontweight="bold" if bold else "normal")
            elif r != "…":
                ax.text(x + w - 0.06, y + rh / 2, f"{pv[r][cols[j - 1]]:,.0f}", fontsize=7, va="center", ha="right", color=NAVY, fontweight="bold" if bold else "normal")
            x += w
    ax.text(x0, 0.3, "Top five provinces shown; the full result is Table 3.5.", fontsize=7.4, color=GREY, style="italic")
    fig.savefig(OUT / "fig_3_2_pivot_layout.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def dashboard():
    fig = plt.figure(figsize=(9.6, 6.3))
    fig.patch.set_facecolor("white")
    fig.text(0.03, 0.955, "Kwacha Basket — 2025 Sales Dashboard", fontsize=14, fontweight="bold", color=NAVY, fontfamily="Playfair Display")
    fig.text(0.03, 0.925, "Source: kb_raw_transactions.xlsx (cleaned, 2,440 lines)", fontsize=7.5, color=GREY)
    kpis = [("Revenue", f"K{EXP['total_revenue'] / 1e6:,.2f}m"), ("Order lines", f"{EXP['lines']:,}"),
            ("Average line", f"K{EXP['avg_line']:,.2f}"), ("Gross margin", f"{EXP['margin_pct']}%")]
    for i, (k, v) in enumerate(kpis):
        ax = fig.add_axes([0.03 + i * 0.235, 0.77, 0.215, 0.12]); ax.axis("off")
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.08", fc=NAVY_T, ec=NAVY, lw=1, transform=ax.transAxes))
        ax.text(0.08, 0.68, k.upper(), fontsize=7, color=GREY, fontweight="bold", transform=ax.transAxes)
        ax.text(0.08, 0.25, v, fontsize=16, color=NAVY, fontweight="bold", transform=ax.transAxes)
    a1 = fig.add_axes([0.13, 0.08, 0.36, 0.6])
    rp = pd.Series(EXP["rev_by_province"]).sort_values()
    a1.barh(rp.index, rp.values / 1000, color=[GOLD if p == "Lusaka" else TEAL for p in rp.index])
    a1.set_title("Revenue by province (K thousand)", fontsize=9, color=NAVY, loc="left", fontweight="bold")
    a2 = fig.add_axes([0.58, 0.43, 0.39, 0.25])
    rm = pd.Series(EXP["rev_by_month"])
    a2.plot(range(12), rm.values / 1000, color=TEAL, lw=2, marker="o", ms=3)
    a2.set_xticks(range(12)); a2.set_xticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    a2.set_title("Revenue by month (K thousand)", fontsize=9, color=NAVY, loc="left", fontweight="bold")
    a3 = fig.add_axes([0.58, 0.08, 0.39, 0.25])
    pm = pd.Series(EXP["rev_by_payment"]).sort_values()
    a3.barh(pm.index, pm.values / pm.sum() * 100, color=NAVY)
    a3.set_title("Share of revenue by payment method (%)", fontsize=9, color=NAVY, loc="left", fontweight="bold")
    for a in (a1, a2, a3):
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
        a.tick_params(labelsize=7.5, colors=GREY)
        a.grid(axis="x" if a is not a2 else "y", color="#E5E7EB", lw=0.6); a.set_axisbelow(True)
    fig.savefig(OUT / "fig_3_3_dashboard.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    before_after(); pivot_layout(); dashboard()
    print("figures written")
