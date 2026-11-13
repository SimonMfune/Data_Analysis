"""Extension idea from Section 9.9: a correlation heatmap for the Quick EDA app.

Paste `correlation_heatmap` into charts.py, add "Correlation heatmap" to the chart
kinds when a file has at least three number columns, and call it with the cleaned data.
Run this file from the repository root to see it on the loans file."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "projects" / "p1_eda_dashboard" / "solution"))
import charts  # noqa: E402
import loader  # noqa: E402


def correlation_heatmap(ax, df, method="spearman", title=None):
    """Lower-triangle heatmap of correlations between number columns, values printed in
    each cell. A diverging colour map centred on zero shows sign and strength."""
    corr = df.select_dtypes("number").corr(method=method)
    mask = np.triu(np.ones_like(corr, dtype=bool))          # hide the duplicate upper half
    image = ax.imshow(corr.mask(mask), cmap="BrBG", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)), corr.columns, rotation=40, ha="right")
    ax.set_yticks(range(len(corr)), corr.columns)
    for i in range(len(corr)):
        for j in range(i):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.grid(False)
    ax.figure.colorbar(image, ax=ax, shrink=0.8, label=f"{method.title()} correlation")
    if title:
        ax.set_title(title)
    return ax


if __name__ == "__main__":
    charts.use_house_style()
    data = loader.load_csv((ROOT / "data/unseen/fintech_loans.csv").read_bytes()).data
    fig, ax = plt.subplots(figsize=(7, 5.5))
    correlation_heatmap(ax, data, title="Loan size rises with income; little else is related")
    out = Path(__file__).with_name("output")
    out.mkdir(exist_ok=True)
    charts.save(fig, out / "ext_correlation_heatmap.png", dpi=150)
    print(data.select_dtypes("number").corr(method="spearman").round(2).to_string())
