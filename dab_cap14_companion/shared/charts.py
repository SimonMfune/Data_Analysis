"""Reusable, house-styled chart functions for Kwacha Basket analyses.

Model answer to the Chapter 8 Challenge exercise, and the chart library used by
Project 1 (Chapter 9). Every function draws on an Axes you pass in (or creates
one), returns that Axes, and never calls plt.show(), so the same code works in
scripts, notebooks and Streamlit.

    import matplotlib.pyplot as plt
    from shared import charts
    charts.use_house_style()
    fig, ax = plt.subplots()
    charts.line(ax, monthly["revenue_zmw"], title="Revenue grew every year", money=True)
    charts.save(fig, "revenue.png")
"""
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

STYLE = Path(__file__).with_name("kb.mplstyle")
TEAL, GOLD, BLUE, CORAL, PURPLE, GREEN = (
    "#0E9AA7", "#A8841A", "#2F5D9E", "#C8553D", "#6B4E9B", "#5E8C31")
INK, MUTED, CONTEXT = "#1B2A41", "#4A5561", "#B8C2CC"
PALETTE = [TEAL, GOLD, BLUE, CORAL, PURPLE, GREEN]


def use_house_style():
    """Apply kb.mplstyle to every chart drawn afterwards in this session."""
    plt.style.use(STYLE)


def kwacha(value, position=None):
    """Format an amount in kwacha for axes and labels: K950, K12k, K1.5m."""
    if abs(value) >= 1_000_000:
        return f"K{value / 1_000_000:.1f}m"
    if abs(value) >= 1_000:
        return f"K{value / 1_000:.0f}k"
    return f"K{value:.0f}"


KWACHA = FuncFormatter(kwacha)


def _finish(ax, title, xlabel, ylabel):
    if title:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    return ax


def line(ax, data, title=None, ylabel=None, money=False, label_ends=True, zero=True):
    """Plot one Series, or each column of a DataFrame, against a datetime index.

    With more than one series, each line is labelled at its right-hand end as well as
    in the legend, so identity never depends on colour alone. Yearly ticks are used
    when the index spans more than two years.
    """
    frame = data.to_frame() if isinstance(data, pd.Series) else data
    for name in frame.columns:
        ax.plot(frame.index, frame[name], label=str(name))
        if label_ends and frame.shape[1] > 1:
            ax.annotate(str(name), xy=(frame.index[-1], frame[name].iloc[-1]),
                        xytext=(6, 0), textcoords="offset points", va="center", fontsize=9)
    if frame.shape[1] > 1:
        ax.legend(loc="upper left")
    if isinstance(frame.index, pd.DatetimeIndex) and (frame.index[-1] - frame.index[0]).days > 730:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    if money:
        ax.yaxis.set_major_formatter(KWACHA)
    if zero:
        ax.set_ylim(0, None)
    return _finish(ax, title, None, ylabel)


def hbar(ax, values, title=None, xlabel=None, highlight=None, money=False, labels=True):
    """Horizontal bars sorted from largest (top) to smallest.

    `highlight` names one or more categories to draw in teal; the rest are grey.
    With no highlight, every bar is teal. Values are written at the end of each bar.
    """
    values = values.sort_values()
    keep = set([highlight] if isinstance(highlight, str) else (highlight or []))
    colours = [TEAL if not keep or name in keep else CONTEXT for name in values.index]
    bars = ax.barh(values.index.astype(str), values.to_numpy(), color=colours, height=0.7)
    if labels:
        text = [kwacha(v) if money else f"{v:,.1f}" for v in values]
        ax.bar_label(bars, labels=text, padding=4, fontsize=9)
        ax.margins(x=0.15)
    if money:
        ax.xaxis.set_major_formatter(KWACHA)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    return _finish(ax, title, xlabel, None)


def histogram(ax, values, bins=40, title=None, xlabel=None, log=False, mark_median=True):
    """Histogram with an optional log x-axis and a labelled median line."""
    values = pd.Series(values).dropna()
    if log:
        import numpy as np
        bins = np.logspace(np.log10(values[values > 0].min()), np.log10(values.max()), bins)
        ax.set_xscale("log")
    ax.hist(values, bins=bins, color=TEAL)
    if mark_median:
        med = values.median()
        ax.axvline(med, color=INK, linewidth=1.2, linestyle="--")
        ax.annotate(f"Median {med:,.0f}", xy=(med, 1), xycoords=("data", "axes fraction"),
                    xytext=(6, -12), textcoords="offset points", fontsize=9)
    ax.set_ylabel("Count")
    return _finish(ax, title, xlabel, None)


def save(fig, path, dpi=300):
    """Save a figure (PNG, SVG or PDF by extension), creating folders as needed, and close it."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return path
