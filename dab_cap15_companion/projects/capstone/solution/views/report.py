"""Page 6, Report: download a summary of the analysis."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the app folder

import streamlit as st  # noqa: E402

import ui  # noqa: E402
from workspace import report  # noqa: E402

st.title("📄 Report")
prep = ui.require("prepared", "Prepare the data first.", "views/prepare.py", "Go to Prepare")
result = st.session_state.get("model")
ins = st.session_state.get("insights")
insight = None
if ins and ins["reply"] is not None and not ins["problems"]:
    insight = (ins["reply"], ins["problems"])
elif ins:
    st.warning("The recommendations failed validation and are not included.")

md = report.build_markdown(st.session_state["dataset"]["name"], prep["df"], prep["log"], result, insight)
png = report.effects_chart_png(result) if result is not None else None
c1, c2 = st.columns(2)
c1.download_button("Download report (HTML)", report.build_html(md, png).encode("utf-8"),
                   file_name="analysis_report.html", mime="text/html", type="primary")
c2.download_button("Download report (Markdown)", md.encode("utf-8"), file_name="analysis_report.md",
                   mime="text/markdown")
st.divider()
st.markdown(md)
