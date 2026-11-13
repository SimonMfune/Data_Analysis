"""Chart functions for the Project 1 dashboard (Milestone M4).

The first part is a copy of shared/charts.py from Chapter 8, so that this folder
can be deployed on its own. The dashboard-specific functions are at the end. Every function draws on an Axes you pass in (or creates
one), returns that Axes, and never calls plt.show(), so the same code works in
scripts, notebooks and Streamlit.

    import matplotlib.pyplot as plt
    import charts
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


# ---------------------------------------------------------------- dashboard additions
MAX_BARS = 15


def bar_counts(ax, s, title=None):
    """Horizontal bars of how often each value occurs; values beyond the top
    MAX_BARS are folded into "Other" so the chart stays readable."""
    counts = s.astype("string").fillna("(missing)").value_counts()
    if len(counts) > MAX_BARS:
        counts = pd.concat([counts.iloc[:MAX_BARS - 1],
                            pd.Series({"Other": counts.iloc[MAX_BARS - 1:].sum()})])
    return hbar(ax, counts.astype(float), title=title, xlabel="Rows", labels=True)


def bar_by(ax, df, category, value, how="sum", title=None):
    """Horizontal bars of a number aggregated (sum, mean or median) within each category."""
    totals = df.groupby(category, observed=True)[value].agg(how).dropna()
    totals = totals.sort_values(ascending=False).head(MAX_BARS)
    money = value.endswith(("_zmw", "_kwacha")) and how == "sum"
    return hbar(ax, totals, title=title, xlabel=f"{how.title()} of {value}", money=money)


def box_by(ax, df, category, value, title=None):
    """Box plots of a number within each category, sorted by median, outliers shown faintly."""
    medians = df.groupby(category, observed=True)[value].median().dropna().sort_values()
    groups = list(medians.index[-MAX_BARS:])
    data = [df.loc[df[category] == g, value].dropna() for g in groups]
    ax.boxplot(data, tick_labels=[str(g) for g in groups], orientation="horizontal",
               widths=0.6, patch_artist=True,
               boxprops={"facecolor": "#BFE6E9", "edgecolor": TEAL},
               medianprops={"color": INK, "linewidth": 1.6},
               flierprops={"markersize": 2, "alpha": 0.3})
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    return _finish(ax, title, value, None)


def scatter(ax, df, x, y, log=False, title=None):
    """Scatter plot of two numbers, with transparency for overlapping points."""
    alpha = 0.6 if len(df) < 1000 else 0.3
    ax.scatter(df[x], df[y], s=12, alpha=alpha, edgecolors="none", color=TEAL)
    if log:
        ax.set_xscale("log")
        ax.set_yscale("log")
    ax.grid(axis="x", visible=True)
    return _finish(ax, title, x, y)


def over_time(ax, df, date, value=None, how="sum", freq="MS", title=None):
    """A line of a number aggregated per period (or a count of rows if value is None)."""
    s = df.set_index(date).sort_index()
    series = s[value].resample(freq).agg(how) if value else s.iloc[:, 0].resample(freq).size()
    ax.plot(series.index, series.values, marker="o" if len(series) <= 24 else None)
    locator = mdates.AutoDateLocator(maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.set_ylim(0, None)
    label = f"{how.title()} of {value}" if value else "Rows"
    return _finish(ax, title, None, label)
