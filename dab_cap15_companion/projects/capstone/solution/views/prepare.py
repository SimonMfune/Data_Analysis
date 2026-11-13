"""Page 2, Prepare: Project 1's configurable cleaning, with a change log."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the app folder

import streamlit as st  # noqa: E402

import ui  # noqa: E402
from workspace import cleaning, profiling  # noqa: E402

st.title("🧹 Prepare")
ds = ui.require("dataset", "Load data first.", "views/data.py", "Go to Data")

c1, c2, c3 = st.columns(3)
options = cleaning.CleaningOptions(
    strip_text=c1.checkbox("Strip spaces from text", True, key="p_strip"),
    placeholders_missing=c1.checkbox("Treat N/A, null, - as missing", False, key="p_ph"),
    drop_duplicates=c2.checkbox("Drop duplicate rows", True, key="p_dup"),
    drop_empty_columns=c2.checkbox("Drop empty columns", True, key="p_empty"),
    numeric_missing=c3.selectbox("Missing numbers", ["leave", "median", "drop rows"], key="p_num"),
    text_missing=c3.selectbox("Missing text", ["leave", "fill Unknown"], key="p_txt"),
)
df, log = cleaning.clean(ds["df"], options)
previous = st.session_state.get("prepared")
if previous is None or previous["options"] != options or previous["source"] != ds["name"]:
    st.session_state["prepared"] = {"df": df, "log": log, "options": options, "source": ds["name"]}
    st.session_state.pop("model", None)
    st.session_state.pop("insights", None)

summary = profiling.profile_dataset(df)
m = st.columns(4)
m[0].metric("Rows", f"{summary['rows']:,}", delta=len(df) - len(ds["df"]) or None, delta_color="off")
m[1].metric("Columns", summary["columns"])
m[2].metric("Missing cells", f"{summary['missing_cells']:,}")
m[3].metric("Duplicate rows", summary["duplicate_rows"])
st.subheader("Change log")
if log.empty:
    st.write("No changes were needed.")
else:
    st.dataframe(log, hide_index=True, width="stretch")
st.subheader("Columns")
st.dataframe(profiling.profile_columns(df), hide_index=True, width="stretch")
st.page_link("views/explore.py", label="Next: explore", icon="➡️")
