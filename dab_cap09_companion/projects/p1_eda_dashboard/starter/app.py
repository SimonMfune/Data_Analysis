"""Project 1: Quick EDA (starter). Run from this folder with:  streamlit run app.py

Work through the milestones in order. Each TODO names its milestone and section.
The app runs at every stage: unfinished parts show a message instead of crashing."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: F401  (needed from M4)
import streamlit as st

import charts
import cleaning
import loader
import profiling

st.set_page_config(page_title="Quick EDA", page_icon="📊", layout="wide")
charts.use_house_style()
SAMPLES = Path(__file__).resolve().parents[3] / "data" / "unseen"

# TODO M5 (Section 9.7): wrap loading and cleaning in @st.cache_data functions.

# ------------------------------------------------------------------ M1: data source (Section 9.3)
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

try:
    result = loader.load_csv(raw)
except NotImplementedError as todo:
    st.warning(f"Not built yet: {todo}")
    st.stop()
except Exception as error:
    st.error(f"Sorry, {name} could not be read as a CSV file: {error}")
    st.stop()
raw_df = result.data

st.title(name)
st.caption(f"Encoding {result.encoding} · delimiter {result.delimiter!r} · {len(raw_df):,} rows")

# TODO M3 (Section 9.5): sidebar expander of cleaning options -> CleaningOptions,
#                        then df, log = cleaning.clean(raw_df, options)
df = raw_df

# TODO M2 (Section 9.4): four st.metric tiles from profiling.profile_dataset(df)

tab_profile, tab_clean, tab_summary, tab_charts, tab_download = st.tabs(
    ["Profile", "Cleaning log", "Summary", "Charts", "Download"])

with tab_profile:
    # TODO M2: show profiling.profile_columns(df), the type-inference notes and df.head(10)
    st.dataframe(df.head(10), width="stretch")

with tab_clean:
    st.info("TODO M3: show the cleaning log and the before-and-after counts.")

with tab_summary:
    st.info("TODO M4 (Section 9.6): numeric summary and top values for a chosen category.")

with tab_charts:
    st.info("TODO M4: chart-type radio, column choosers, and a chart from charts.py.")

with tab_download:
    st.info("TODO M5: download buttons for the cleaned data and the cleaning log.")
