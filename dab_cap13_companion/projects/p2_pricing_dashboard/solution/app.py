"""Price Advisor: suggested list prices for new products (Project 2).

Run from this folder:   python train.py        (once, and after every retraining)
                        streamlit run app.py
This file only sets up the page and the navigation; each page lives in views/."""
import streamlit as st

st.set_page_config(page_title="Price Advisor", page_icon="🏷️", layout="wide")
pages = [
    st.Page("views/suggest.py", title="Suggest a price", icon="🏷️", default=True),
    st.Page("views/what_if.py", title="What-if", icon="🎚️"),
    st.Page("views/model_card.py", title="Model card", icon="📋"),
    st.Page("views/batch.py", title="Batch scoring", icon="📄"),
]
st.navigation(pages).run()
