"""AI-Enhanced Predictive Analytics Workspace (Chapter 15 capstone).

Run from this folder:   streamlit run app.py
Each page lives in views/; the analysis code lives in the workspace package."""
import streamlit as st

import ui

st.set_page_config(page_title="Analytics Workspace", page_icon="🧭", layout="wide")
ui.secrets_to_environment()
pages = [
    st.Page("views/data.py", title="1 Data", icon="📥", default=True),
    st.Page("views/prepare.py", title="2 Prepare", icon="🧹"),
    st.Page("views/explore.py", title="3 Explore", icon="🔎"),
    st.Page("views/model.py", title="4 Model", icon="📈"),
    st.Page("views/insights.py", title="5 Insights", icon="💡"),
    st.Page("views/report.py", title="6 Report", icon="📄"),
]
st.navigation(pages).run()
with st.sidebar:
    if "dataset" in st.session_state:
        st.caption(f"Dataset: **{st.session_state['dataset']['name']}**")
    if "model" in st.session_state:
        m = st.session_state["model"]
        st.caption(f"Model: {m.kind} regression of **{m.target}**")
