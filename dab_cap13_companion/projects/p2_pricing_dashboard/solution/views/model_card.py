"""Milestone M4: what the model is, how well it works, and when not to use it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import common  # noqa: E402

artefact = common.start_page()
plt.style.use(Path(__file__).resolve().parents[1] / "kb.mplstyle")
m = artefact["metrics"]
st.title("Model card")
st.write("**Purpose.** A starting list price for a new product, for a pricing analyst to review. "
         "The model does not set prices on its own.")

c = st.columns(4)
c[0].metric("Typical error (CV MAPE)", f"{m['cv_MAPE']:.1%}")
c[1].metric("Test MAPE", f"{m['test_MAPE']:.1%}")
c[2].metric("Test R²", f"{m['test_R2']:.3f}")
c[3].metric(f"Test prices inside {artefact['coverage']:.0%} range", f"{m['interval_coverage_test']:.0%}")

left, right = st.columns(2)
with left:
    st.subheader("Errors on the test set")
    tp = artefact["test_predictions"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(tp["predicted"], (tp["actual"] - tp["predicted"]) / tp["actual"] * 100,
               s=14, alpha=0.6, color="#0E9AA7", edgecolors="none")
    ax.axhline(0, color="#1B2A41", linewidth=1)
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter("K{x:,.0f}")
    ax.set_xlabel("Model price (log scale)")
    ax.set_ylabel("Error as % of actual price")
    st.pyplot(fig)
    plt.close(fig)
with right:
    st.subheader("What moves the price")
    effects = artefact["effects"]
    pct = (np.exp(effects.drop(["unit_cost_zmw", "weight_kg"])) - 1) * 100
    table = pd.DataFrame({"Feature": [n.replace("category_", "Category: ").replace("brand_tier_", "Tier: ")
                                      .replace("imported_flag", "Imported") for n in pct.index],
                          "Effect on price (%)": pct.round(1).to_numpy()}).sort_values("Effect on price (%)")
    st.dataframe(table, hide_index=True, width="stretch")
    st.caption(f"Compared with Baby & Kids and Premium. A 10% higher cost gives about "
               f"{effects['unit_cost_zmw'] * 10:.1f}% higher price.")

st.subheader("Limitations")
lo, hi = artefact["cost_range"]
st.markdown(f"""
- Learns from current prices, so it repeats today's pricing policy, including its mistakes.
- Knows nothing about competitors, demand, promotions or exchange rates.
- Trained on unit costs from K{lo:,.2f} to K{hi:,.2f}; outside that range it extrapolates.
- Effects are associations in past pricing, not proof of what customers will pay.
""")
st.caption(f"Trained {artefact['trained_at']} on {artefact['training_rows']} products · "
           + " · ".join(f"{k} {v}" for k, v in artefact["versions"].items()))
