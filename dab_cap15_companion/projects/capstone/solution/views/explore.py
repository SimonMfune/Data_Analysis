"""Page 3, Explore: summaries and charts from Project 1."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the app folder

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import streamlit as st  # noqa: E402

import ui  # noqa: E402
from workspace import charts, profiling  # noqa: E402

st.title("🔎 Explore")
prep = ui.require("prepared", "Prepare the data first.", "views/prepare.py", "Go to Prepare")
df = prep["df"]
charts.use_house_style()
profile = profiling.profile_columns(df)
numbers = profile.loc[profile["role"] == "number", "column"].tolist()
categories = profile.loc[profile["role"].isin(["category", "text"]) & (profile["distinct"] <= 30), "column"].tolist()

left, right = st.columns([1, 2])
with left:
    st.subheader("Numbers")
    st.dataframe(profiling.numeric_summary(df).round(2)[["mean", "median", "std", "skew"]], width="stretch")
with right:
    kinds = (["Histogram"] if numbers else []) + (["Box plot by category"] if numbers and categories else []) \
        + (["Scatter"] if len(numbers) > 1 else []) + (["Bar: counts"] if categories else [])
    if kinds:
        kind = st.radio("Chart", kinds, horizontal=True, key="ex_kind")
        fig, ax = plt.subplots(figsize=(8, 4))
        if kind == "Histogram":
            col = st.selectbox("Number", numbers, key="ex_hist")
            charts.histogram(ax, df[col], title=f"Distribution of {col}", xlabel=col)
        elif kind == "Box plot by category":
            c1, c2 = st.columns(2)
            cat = c1.selectbox("Category", categories, key="ex_box_cat")
            val = c2.selectbox("Number", numbers, key="ex_box_val")
            charts.box_by(ax, df, cat, val, title=f"{val} by {cat}")
        elif kind == "Scatter":
            c1, c2 = st.columns(2)
            x = c1.selectbox("x", numbers, key="ex_x")
            y = c2.selectbox("y", numbers, index=1, key="ex_y")
            charts.scatter(ax, df, x, y, title=f"{y} against {x}")
        else:
            col = st.selectbox("Category", categories, key="ex_count")
            charts.bar_counts(ax, df[col], title=f"Rows by {col}")
        st.pyplot(fig)
        plt.close(fig)
st.page_link("views/model.py", label="Next: model", icon="➡️")
