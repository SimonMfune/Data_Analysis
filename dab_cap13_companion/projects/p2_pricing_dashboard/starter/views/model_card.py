"""M4 (Section 13.6): metrics, a residual plot from the saved test predictions, the effects table and the limitations."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

import common  # noqa: E402

artefact = common.start_page()
st.title("Model card")
st.info("TODO M4: metrics, a residual plot from the saved test predictions, the effects table and the limitations.")
