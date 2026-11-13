"""Shared Streamlit pieces for every page: the cached artefact and the error caption."""
import streamlit as st

import serving


@st.cache_resource(show_spinner="Loading the pricing model...")
def get_artefact() -> dict:
    """Load the model once per server process and share it between users and pages."""
    return serving.load_artefact()


def start_page() -> dict:
    """Return the artefact, or stop the page with a clear message if it is missing."""
    try:
        return get_artefact()
    except FileNotFoundError as error:
        st.error(f"The model has not been trained yet. {error}")
        st.stop()


def typical_error_caption(artefact: dict) -> str:
    """Rule 3: the typical error, shown beside every suggestion."""
    m = artefact["metrics"]
    lo, hi = artefact["interval_log_quantiles"]
    return (f"Typical error about {m['cv_MAPE']:.0%} of the price. "
            f"The range shows where {artefact['coverage']:.0%} of similar products' prices fall "
            f"(model price ×{2.718281828 ** lo:.2f} to ×{2.718281828 ** hi:.2f}).")
