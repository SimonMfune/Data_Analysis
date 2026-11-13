"""M2 (Section 13.4): a form for one product; show the suggested price, the range and the margin, with the typical-error caption (rule 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

import common  # noqa: E402

artefact = common.start_page()
st.title("Suggest")
st.info("TODO M2: a form for one product; show the suggested price, the range and the margin, with the typical-error caption (rule 3).")
