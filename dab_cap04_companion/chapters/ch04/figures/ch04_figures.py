"""Chapter 4 figures (300 DPI): the Kwacha Basket ERD and JOIN types.

Run from the repository root:  python chapters/ch04/figures/ch04_figures.py
"""
import sqlite3
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

for f in list(Path("/usr/share/fonts/opentype/inter").glob("Inter-*.otf")) + list(Path.home().joinpath(".fonts").glob("*.ttf")):
    fm.fontManager.addfont(str(f))
NAVY, TEAL, GOLD = "#1B2A41", "#0E9AA7", "#C9A227"
TEAL_T, GOLD_T, NAVY_T, GREY = "#E6F4F5", "#FAF3DE", "#E8ECF2", "#4B5563"
plt.rcParams.update({"font.family": "Inter", "font.size": 9})
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
con = sqlite3.connect(ROOT / "data" / "kwacha_basket.db")
count = lambda t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]

TABLES = {  # name: (x, y, [(column, role)])  role: PK, FK, PK/FK or ''
    "campaigns": (4.35, 9.0, [("campaign_id", "PK"), ("channel", ""), ("start_date", ""), ("budget_zmw", "")]),
    "customers": (0.2, 6.2, [("customer_id", "PK"), ("first_name", ""), ("province", ""), ("signup_date", ""), ("…", "")]),
    "orders": (4.35, 6.2, [("order_id", "PK"), ("customer_id", "FK"), ("campaign_id", "FK"), ("order_datetime", ""), ("status", ""), ("…", "")]),
    "payments": (8.5, 7.55, [("payment_id", "PK"), ("order_id", "FK"), ("method", ""), ("amount_zmw", "")]),
    "deliveries": (8.5, 4.75, [("order_id", "PK/FK"), ("courier", ""), ("delivered_at", ""), ("delayed_flag", "")]),
    "order_items": (4.35, 2.85, [("order_id", "PK/FK"), ("line_no", "PK"), ("product_id", "FK"), ("quantity", ""), ("unit_price_zmw", "")]),
    "returns": (8.5, 1.95, [("return_id", "PK"), ("order_id", "FK"), ("product_id", "FK"), ("refund_zmw", "")]),
    "reviews": (0.2, 3.2, [("review_id", "PK"), ("order_id", "FK"), ("product_id", "FK"), ("rating", "")]),
    "products": (4.35, -0.35, [("product_id", "PK"), ("supplier_id", "FK"), ("category", ""), ("list_price_zmw", "")]),
    "suppliers": (0.2, -0.35, [("supplier_id", "PK"), ("supplier_name", ""), ("country", "")]),
}
W, RH, HH = 2.75, 0.27, 0.42


def erd():
    fig, ax = plt.subplots(figsize=(9.4, 9.6))
    ax.set_xlim(-0.1, 11.4); ax.set_ylim(-2.35, 10.15); ax.axis("off")
    geo = {}
    for name, (x, y, cols) in TABLES.items():
        h = HH + RH * len(cols)
        geo[name] = (x, y, h)
        ax.add_patch(FancyBboxPatch((x, y - h), W, h, boxstyle="round,pad=0,rounding_size=0.06", fc="white", ec=NAVY, lw=1.3, zorder=3))
        ax.add_patch(Rectangle((x, y - HH), W, HH, fc=NAVY, ec=NAVY, zorder=3))
        ax.text(x + 0.12, y - HH / 2, name, color="white", fontsize=9.5, fontweight="bold", va="center", zorder=4, family="Fira Code")
        ax.text(x + W - 0.1, y - HH / 2, f"{count(name):,}", color="#C9D3E3", fontsize=7, va="center", ha="right", zorder=4)
        for i, (c, role) in enumerate(cols):
            cy = y - HH - RH * (i + 0.5)
            col = {"PK": GOLD, "FK": TEAL, "PK/FK": GOLD}.get(role, None)
            if role:
                ax.text(x + 0.12, cy, role, fontsize=6.3, fontweight="bold", va="center", color=col, zorder=4)
            ax.text(x + 0.62, cy, c, fontsize=7.6, va="center", color=NAVY, zorder=4, family="Fira Code",
                    fontweight="bold" if "PK" in role else "normal")

    def port(name, side, frac=0.5):
        x, y, h = geo[name]
        return {"l": (x, y - h * frac), "r": (x + W, y - h * frac), "t": (x + W * frac, y), "b": (x + W * frac, y - h)}[side]

    def link(a, b, one, many, mid=None, many_sym="∞"):
        (x1, y1), (x2, y2) = a, b
        pts = [(x1, y1)] + (mid or []) + [(x2, y2)]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GREY, lw=1.2, zorder=1)
        ax.text(*one, "1", fontsize=8, color=NAVY, fontweight="bold", ha="center", va="center", zorder=5,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
        ax.text(*many, many_sym, fontsize=10 if many_sym == "∞" else 8, color=NAVY, fontweight="bold", ha="center", va="center", zorder=5,
                bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none"))

    a, b = port("customers", "r", 0.25), port("orders", "l", 0.25)
    link(a, b, (a[0] + 0.18, a[1] + 0.14), (b[0] - 0.2, b[1] + 0.14))
    a, b = port("campaigns", "b"), port("orders", "t")
    link(a, b, (a[0] + 0.15, a[1] - 0.2), (b[0] + 0.15, b[1] + 0.2))
    a, b = port("orders", "r", 0.2), port("payments", "l", 0.4)
    link(a, b, (a[0] + 0.18, a[1] + 0.14), (b[0] - 0.2, b[1] + 0.14), mid=[(7.8, a[1]), (7.8, b[1])])
    a, b = port("orders", "r", 0.6), port("deliveries", "l", 0.3)
    link(a, b, (a[0] + 0.18, a[1] + 0.14), (b[0] - 0.2, b[1] + 0.14), mid=[(7.6, a[1]), (7.6, b[1])], many_sym="1")
    a, b = port("orders", "b"), port("order_items", "t")
    link(a, b, (a[0] + 0.15, a[1] - 0.17), (b[0] + 0.15, b[1] + 0.2))
    a, b = port("products", "t"), port("order_items", "b")
    link(a, b, (a[0] + 0.15, a[1] + 0.17), (b[0] + 0.15, b[1] - 0.2))
    a, b = port("suppliers", "r", 0.4), port("products", "l", 0.4)
    link(a, b, (a[0] + 0.18, a[1] + 0.14), (b[0] - 0.2, b[1] + 0.14))
    a, b = port("orders", "r", 0.9), port("returns", "l", 0.25)
    link(a, b, (a[0] + 0.18, a[1] + 0.14), (b[0] - 0.2, b[1] + 0.14), mid=[(7.4, a[1]), (7.4, b[1])])
    a, b = port("products", "r", 0.3), port("returns", "b", 0.5)
    link(a, b, (a[0] + 0.18, a[1] + 0.14), (b[0] + 0.15, b[1] - 0.2), mid=[(b[0], a[1])])
    a, b = port("orders", "l", 0.85), port("reviews", "r", 0.25)
    link(a, b, (a[0] - 0.18, a[1] + 0.14), (b[0] + 0.2, b[1] + 0.14), mid=[(3.6, a[1]), (3.6, b[1])])
    a, b = port("products", "l", 0.13), port("reviews", "r", 0.8)
    link(a, b, (a[0] - 0.18, a[1] + 0.14), (b[0] + 0.2, b[1] + 0.14), mid=[(3.35, a[1]), (3.35, b[1])])
    ax.text(5.6, -2.25, "PK primary key   ·   FK foreign key   ·   1 — ∞ one-to-many   ·   figures in headers are row counts",
            ha="center", fontsize=7.6, color=GREY, style="italic")
    fig.savefig(OUT / "fig_4_1_erd.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def joins():
    total = count("customers")
    none = con.execute("SELECT COUNT(*) FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)").fetchone()[0]
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.6))
    specs = [("INNER JOIN", "Customers who have orders", f"{total - none:,} customers", "inner"),
             ("LEFT JOIN", "Every customer, with orders where they exist", f"{total:,} customers", "left"),
             ("LEFT JOIN … WHERE o.order_id IS NULL", "Customers with no orders at all", f"{none:,} customers", "anti")]
    for ax, (title, sub, n, kind) in zip(axes, specs):
        ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.75, 1.75); ax.set_aspect("equal"); ax.axis("off")
        L, R = Circle((-0.55, 0), 1.0), Circle((0.55, 0), 1.0)
        fillL = TEAL if kind in ("left", "anti") else "white"
        ax.add_patch(Circle((-0.55, 0), 1.0, fc=fillL, ec=NAVY, lw=1.5, alpha=0.9))
        ax.add_patch(Circle((0.55, 0), 1.0, fc="white", ec=NAVY, lw=1.5, alpha=0.0))
        if kind in ("inner", "left"):
            import numpy as np
            t = np.linspace(-np.pi / 2.0, np.pi / 2.0, 200)
            # lens shape: intersection of the two circles
            th = np.arccos(0.55)
            a1 = np.linspace(-th, th, 100); a2 = np.linspace(np.pi - th, np.pi + th, 100)
            xs = list(-0.55 + np.cos(a1)) + list(0.55 + np.cos(a2))
            ys = list(np.sin(a1)) + list(np.sin(a2))
            ax.fill(xs, ys, color=GOLD if kind == "inner" else TEAL, alpha=0.95, zorder=2)
        if kind == "anti":
            import numpy as np
            th = np.arccos(0.55)
            a1 = np.linspace(-th, th, 100); a2 = np.linspace(np.pi - th, np.pi + th, 100)
            xs = list(-0.55 + np.cos(a1)) + list(0.55 + np.cos(a2)); ys = list(np.sin(a1)) + list(np.sin(a2))
            ax.fill(xs, ys, color="white", zorder=2)
        ax.add_patch(Circle((-0.55, 0), 1.0, fc="none", ec=NAVY, lw=1.5, zorder=3))
        ax.add_patch(Circle((0.55, 0), 1.0, fc="none", ec=NAVY, lw=1.5, zorder=3))
        ax.text(-1.05, 0, "customers", ha="center", va="center", fontsize=7.4, color=NAVY if kind == "inner" else "white", fontweight="bold", zorder=4, rotation=90)
        ax.text(1.05, 0, "orders", ha="center", va="center", fontsize=7.4, color=NAVY, fontweight="bold", zorder=4, rotation=90)
        ax.text(0, 1.5, title, ha="center", fontsize=8.6, fontweight="bold", color=NAVY, family="Fira Code")
        ax.text(0, -1.3, sub, ha="center", fontsize=7.4, color=GREY)
        ax.text(0, -1.62, n, ha="center", fontsize=8.4, color=NAVY, fontweight="bold")
    fig.savefig(OUT / "fig_4_2_joins.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    erd(); joins()
    print("figures written to", OUT)
