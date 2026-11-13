"""Milestone M3: how the suggested price and margin respond to cost, tier and origin."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))    # the solution folder

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import common  # noqa: E402
import serving  # noqa: E402
from features import CATEGORIES, TIERS  # noqa: E402

artefact = common.start_page()
plt.style.use(Path(__file__).resolve().parents[1] / "kb.mplstyle")
st.title("What-if analysis")
start = st.session_state.get("product", {"category": "Groceries", "brand_tier": "Value",
                                         "imported_flag": 0, "weight_kg": 2.0, "unit_cost_zmw": 45.0})

c1, c2, c3 = st.columns(3)
category = c1.selectbox("Category", CATEGORIES, index=CATEGORIES.index(start["category"]), key="wi_cat")
imported = c2.toggle("Imported", value=bool(start["imported_flag"]), key="wi_imp")
weight = c3.number_input("Weight (kg)", 0.01, 100.0, float(start["weight_kg"]), key="wi_w")
cost = st.slider("Unit cost (K)", 1.0, max(500.0, float(start["unit_cost_zmw"]) * 3),
                 float(start["unit_cost_zmw"]), step=1.0, key="wi_cost")

rows = pd.DataFrame([{"category": category, "brand_tier": t, "imported_flag": int(imported),
                      "weight_kg": weight, "unit_cost_zmw": cost} for t in TIERS])
table = serving.suggest(artefact, rows)
st.subheader("The same product in each brand tier")
st.dataframe(table[["brand_tier", "suggested_price_zmw", "low_zmw", "high_zmw", "margin_pct"]],
             hide_index=True, width="stretch",
             column_config={"brand_tier": "Tier", "suggested_price_zmw": st.column_config.NumberColumn(
                 "Suggested", format="K%.2f"), "low_zmw": st.column_config.NumberColumn("Range from", format="K%.2f"),
                 "high_zmw": st.column_config.NumberColumn("Range to", format="K%.2f"),
                 "margin_pct": st.column_config.NumberColumn("Margin", format="%.1f%%")})
st.caption(common.typical_error_caption(artefact))

st.subheader("Suggested price across a range of costs")
costs = np.linspace(max(1.0, cost * 0.5), cost * 1.5, 40)
grid = pd.DataFrame([{"category": category, "brand_tier": t, "imported_flag": int(imported),
                      "weight_kg": weight, "unit_cost_zmw": c} for t in TIERS for c in costs])
priced = serving.suggest(artefact, grid)
fig, ax = plt.subplots(figsize=(8, 3.8))
for tier in TIERS:
    part = priced[priced["brand_tier"] == tier]
    ax.plot(part["unit_cost_zmw"], part["model_price_zmw"], label=tier)
ax.plot(costs, costs * 1.10, color="#C8553D", linestyle="--", linewidth=1, label="cost + 10% (floor)")
ax.axvline(cost, color="#9AA5B1", linewidth=0.8)
ax.set_xlabel("Unit cost (K)")
ax.set_ylabel("Model price (K)")
ax.set_title(f"{category}, {'imported' if imported else 'local'}, {weight:g} kg")
ax.legend(ncols=4, loc="upper left")
st.pyplot(fig)
plt.close(fig)
