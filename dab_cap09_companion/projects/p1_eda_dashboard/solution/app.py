"""Project 1: Quick EDA, an interactive dashboard that profiles, cleans, summarises
and charts any CSV file.  Run from this folder with:  streamlit run app.py"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

import charts
import cleaning
import loader
import profiling

st.set_page_config(page_title="Quick EDA", page_icon="📊", layout="wide")
charts.use_house_style()
SAMPLES = Path(__file__).resolve().parents[3] / "data" / "unseen"


# ------------------------------------------------------------------ cached work (M5)
@st.cache_data(show_spinner="Reading the file...")
def load(raw: bytes) -> loader.LoadResult:
    return loader.load_csv(raw)


@st.cache_data(show_spinner="Cleaning...")
def run_cleaning(df, options: cleaning.CleaningOptions):
    return cleaning.clean(df, options)


@st.cache_data
def to_csv_bytes(df) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


# ------------------------------------------------------------------ sidebar: data source (M1)
st.sidebar.title("📊 Quick EDA")
uploaded = st.sidebar.file_uploader("Upload a CSV file", type=["csv", "txt"])
samples = sorted(p.name for p in SAMPLES.glob("*.csv")) if SAMPLES.exists() else []
sample = None
if uploaded is None and samples:
    sample = st.sidebar.selectbox("...or try a sample file", ["(none)"] + samples, key="sample")

if uploaded is not None:
    name, raw = uploaded.name, uploaded.getvalue()
elif sample and sample != "(none)":
    name, raw = sample, (SAMPLES / sample).read_bytes()
else:
    st.title("Quick EDA")
    st.info("Upload a CSV file in the sidebar, or choose a sample, to profile, clean and chart it.")
    st.stop()

# A new file has different columns, so forget the chart choices made for the old one.
if st.session_state.get("source") != name:
    for key in [k for k in st.session_state if k.startswith("chart_")]:
        del st.session_state[key]
    st.session_state["source"] = name

try:
    result = load(raw)
except Exception as error:                 # a file we cannot read must not crash the app
    st.error(f"Sorry, {name} could not be read as a CSV file: {error}")
    st.stop()
raw_df = result.data
if raw_df.empty:
    st.warning(f"{name} has a header row but no data.")
    st.stop()

# ------------------------------------------------------------------ sidebar: cleaning (M3)
with st.sidebar.expander("Cleaning options", expanded=True):
    options = cleaning.CleaningOptions(
        strip_text=st.checkbox("Strip spaces from text", True),
        placeholders_missing=st.checkbox("Treat N/A, null, - as missing", False,
                                         help="Off by default: in some files these are real values."),
        drop_duplicates=st.checkbox("Drop duplicate rows", True),
        drop_empty_columns=st.checkbox("Drop empty columns", True),
        numeric_missing=st.selectbox("Missing numbers", ["leave", "median", "drop rows"],
                                     key="opt_numeric"),
        text_missing=st.selectbox("Missing text", ["leave", "fill Unknown"], key="opt_text"),
    )
df, log = run_cleaning(raw_df, options)

# ------------------------------------------------------------------ header
st.title(name)
st.caption(f"Encoding {result.encoding} · delimiter {result.delimiter!r} · "
           f"{len(raw_df):,} rows read, {len(df):,} after cleaning")
summary = profiling.profile_dataset(df)
cols = st.columns(4)
cols[0].metric("Rows", f"{summary['rows']:,}", delta=len(df) - len(raw_df) or None,
                  delta_color="off")
cols[1].metric("Columns", summary["columns"])
cols[2].metric("Missing cells", f"{summary['missing_cells']:,}")
cols[3].metric("Duplicate rows", summary["duplicate_rows"])

profile = profiling.profile_columns(df)
numbers = profile.loc[profile["role"] == "number", "column"].tolist()
dates = profile.loc[profile["role"] == "date", "column"].tolist()
categories = profile.loc[(profile["role"].isin(["category", "text"])) &
                         (profile["distinct"] <= 50), "column"].tolist()

tab_profile, tab_clean, tab_summary, tab_charts, tab_download = st.tabs(
    ["Profile", "Cleaning log", "Summary", "Charts", "Download"])

# ------------------------------------------------------------------ M2: profile
with tab_profile:
    st.subheader("Columns")
    st.dataframe(profile, hide_index=True, width="stretch",
                 column_config={"missing_pct": st.column_config.ProgressColumn(
                     "missing %", format="%.1f%%", min_value=0, max_value=100)})
    with st.expander("How each column's type was decided"):
        st.write("\n".join(f"- {note}" for note in result.notes) or "No columns were converted.")
    st.subheader("First rows")
    st.dataframe(df.head(10), width="stretch")

# ------------------------------------------------------------------ M3: cleaning log
with tab_clean:
    if log.empty:
        st.success("The chosen cleaning steps found nothing to change.")
    else:
        st.dataframe(log, hide_index=True, width="stretch")
    before, after = int(raw_df.isna().sum().sum()), int(df.isna().sum().sum())
    st.write(f"Rows: {len(raw_df):,} → {len(df):,}. Missing cells: {before:,} → {after:,}.")

# ------------------------------------------------------------------ M4: summary
with tab_summary:
    if numbers:
        st.subheader("Numbers")
        st.dataframe(profiling.numeric_summary(df).round(2), width="stretch")
    if categories:
        st.subheader("Categories")
        chosen = st.selectbox("Column", categories, key="chart_summary_col")
        st.dataframe(profiling.top_values(df[chosen]), width="stretch")

# ------------------------------------------------------------------ M4: charts
with tab_charts:
    kinds = []
    if numbers:
        kinds += ["Histogram"]
    if categories:
        kinds += ["Bar: counts"]
    if categories and numbers:
        kinds += ["Bar: total by category", "Box plot by category"]
    if len(numbers) >= 2:
        kinds += ["Scatter"]
    if dates:
        kinds += ["Over time"]
    if not kinds:
        st.info("This file has no number, date or category columns to chart.")
    else:
        kind = st.radio("Chart", kinds, horizontal=True, key="chart_kind")
        fig, ax = plt.subplots(figsize=(8, 4.2))
        if kind == "Histogram":
            col = st.selectbox("Number", numbers, key="chart_hist_col")
            log_x = st.checkbox("Log scale", key="chart_hist_log",
                                disabled=bool((df[col].dropna() <= 0).any()))
            charts.histogram(ax, df[col], title=f"Distribution of {col}", xlabel=col, log=log_x)
        elif kind == "Bar: counts":
            col = st.selectbox("Category", categories, key="chart_count_col")
            charts.bar_counts(ax, df[col], title=f"Rows by {col}")
        elif kind == "Bar: total by category":
            c1, c2, c3 = st.columns(3)
            cat = c1.selectbox("Category", categories, key="chart_by_cat")
            val = c2.selectbox("Number", numbers, key="chart_by_val")
            how = c3.selectbox("Aggregate", ["sum", "mean", "median"], key="chart_by_how")
            charts.bar_by(ax, df, cat, val, how, title=f"{how.title()} of {val} by {cat}")
        elif kind == "Box plot by category":
            c1, c2 = st.columns(2)
            cat = c1.selectbox("Category", categories, key="chart_box_cat")
            val = c2.selectbox("Number", numbers, key="chart_box_val")
            charts.box_by(ax, df, cat, val, title=f"{val} by {cat}")
        elif kind == "Scatter":
            c1, c2, c3 = st.columns([2, 2, 1])
            x = c1.selectbox("x", numbers, key="chart_sc_x")
            y = c2.selectbox("y", numbers, index=min(1, len(numbers) - 1), key="chart_sc_y")
            positive = bool((df[[x, y]].dropna() > 0).all().all())
            log_xy = c3.checkbox("Log scales", key="chart_sc_log", disabled=not positive)
            charts.scatter(ax, df, x, y, log=log_xy, title=f"{y} against {x}")
            st.caption(f"Pearson r = {df[x].corr(df[y]):.2f} · "
                       f"Spearman ρ = {df[x].corr(df[y], method='spearman'):.2f}")
        elif kind == "Over time":
            c1, c2, c3, c4 = st.columns(4)
            date = c1.selectbox("Date", dates, key="chart_t_date")
            val = c2.selectbox("Number", ["(count rows)"] + numbers, key="chart_t_val")
            how = c3.selectbox("Aggregate", ["sum", "mean"], key="chart_t_how",
                               disabled=val == "(count rows)")
            freq = {"Month": "MS", "Week": "W", "Day": "D"}[
                c4.selectbox("Period", ["Month", "Week", "Day"], key="chart_t_freq")]
            charts.over_time(ax, df.dropna(subset=[date]), date,
                             None if val == "(count rows)" else val, how, freq,
                             title=f"{'Rows' if val == '(count rows)' else val} over time")
        st.pyplot(fig)
        plt.close(fig)

# ------------------------------------------------------------------ M5: download
with tab_download:
    stem = Path(name).stem
    st.download_button("Download cleaned data (CSV)", to_csv_bytes(df),
                       file_name=f"{stem}_clean.csv", mime="text/csv")
    st.download_button("Download cleaning log (CSV)", to_csv_bytes(log),
                       file_name=f"{stem}_cleaning_log.csv", mime="text/csv")
    st.caption("The cleaned file is UTF-8 and comma-separated, whatever the original used.")
