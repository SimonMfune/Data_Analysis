"""Exercise 10.2, Streamlit version. Run from the repository root:
    streamlit run chapters/ch10/solutions/ex10_2_bayes_app.py"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from ex10_2_bayes_calculator import p_fraud_given_flag  # noqa: E402

st.title("How likely is a flagged payment to be fraud?")
base = st.slider("Base rate: share of payments that are fraud (%)", 0.1, 20.0, 0.5, 0.1) / 100
sens = st.slider("Sensitivity: share of frauds the system flags (%)", 50, 100, 90) / 100
fa = st.slider("False-alarm rate: share of genuine payments flagged (%)", 0.5, 10.0, 3.0, 0.5) / 100
post = p_fraud_given_flag(base, sens, fa)
st.metric("P(fraud | flag)", f"{post:.1%}")
n = 10_000
st.write(f"Of {n:,} payments, about {n * base * sens:,.0f} frauds and "
         f"{n * (1 - base) * fa:,.0f} genuine payments are flagged.")
