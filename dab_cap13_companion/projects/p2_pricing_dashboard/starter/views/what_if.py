"""M3 (Section 13.5): sliders for cost, tier and origin; a tier comparison table and a price-versus-cost chart with the cost + 10% floor."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

import common  # noqa: E402

artefact = common.start_page()
st.title("What if")
st.info("TODO M3: sliders for cost, tier and origin; a tier comparison table and a price-versus-cost chart with the cost + 10% floor.")
