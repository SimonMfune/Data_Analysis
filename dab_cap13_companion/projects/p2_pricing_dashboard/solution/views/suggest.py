"""Milestone M2: one product in, a suggested price with a range out."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))    # the solution folder

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import common  # noqa: E402
import serving  # noqa: E402
from features import CATEGORIES, TIERS  # noqa: E402

artefact = common.start_page()
st.title("🏷️ Suggest a price")
st.write("Describe a new product to get a suggested list price, the range it is likely to fall in, "
         "and the margin it would earn.")

with st.form("product_form"):
    c1, c2 = st.columns(2)
    category = c1.selectbox("Category", CATEGORIES, index=CATEGORIES.index("Groceries"))
    tier = c2.selectbox("Brand tier", TIERS)
    cost = c1.number_input("Unit cost (K)", min_value=1.0, max_value=50_000.0, value=45.0, step=1.0)
    weight = c2.number_input("Weight (kg)", min_value=0.01, max_value=100.0, value=2.0, step=0.1)
    imported = st.toggle("Imported", value=False)
    submitted = st.form_submit_button("Suggest price", type="primary")

if submitted:
    st.session_state["product"] = {"category": category, "brand_tier": tier,
                                   "imported_flag": int(imported), "weight_kg": weight,
                                   "unit_cost_zmw": cost}

if "product" in st.session_state:
    row = serving.suggest(artefact, pd.DataFrame([st.session_state["product"]])).iloc[0]
    lo_c, hi_c = artefact["cost_range"]
    if not lo_c <= row["unit_cost_zmw"] <= hi_c:
        st.warning(f"Unit cost K{row['unit_cost_zmw']:,.2f} is outside the training range "
                   f"(K{lo_c:,.2f} to K{hi_c:,.2f}); treat this suggestion with extra caution.")
    m1, m2, m3 = st.columns(3)
    m1.metric("Suggested list price", f"K{row['suggested_price_zmw']:,.2f}")
    m2.metric("Likely range", f"K{row['low_zmw']:,.2f} – K{row['high_zmw']:,.2f}")
    m3.metric("Gross margin at suggested price", f"{row['margin_pct']:.1f}%")
    st.caption(common.typical_error_caption(artefact))
    if row["notes"]:
        st.info(row["notes"])
    with st.expander("How the suggestion was made"):
        st.write(f"- Model price: K{row['model_price_zmw']:,.2f}\n"
                 f"- Rule 1: never below cost + 10% (K{row['unit_cost_zmw'] * 1.10:,.2f})\n"
                 f"- Rule 2: rounded to a price ending in .00, .50 or .99\n"
                 f"- Rule 3: the typical error and range are shown above")
    st.session_state["last_suggestion"] = float(row["suggested_price_zmw"])
