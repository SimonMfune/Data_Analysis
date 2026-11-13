"""M5 (Section 13.7): upload a CSV, validate it, list problems by row, score the good rows and offer a download."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

import common  # noqa: E402

artefact = common.start_page()
st.title("Batch")
st.info("TODO M5: upload a CSV, validate it, list problems by row, score the good rows and offer a download.")
