"""Page 4, Model: choose a target and features, fit, and read the metrics."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the app folder

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import streamlit as st  # noqa: E402

import ui  # noqa: E402
from workspace import modelling, report  # noqa: E402

st.title("📈 Model")
prep = ui.require("prepared", "Prepare the data first.", "views/prepare.py", "Go to Prepare")
df = prep["df"]


@st.cache_data(show_spinner="Fitting and cross-validating...")
def fit_cached(df, target, features, kind):
    return modelling.fit(df, target, list(features), kind)


candidates = [c for c in df.columns if df[c].nunique() == 2 or (df[c].dtype.kind in "if" and df[c].nunique() > 2)]
target = st.selectbox("Target: what to predict", candidates, key="m_target")
try:
    suggested = modelling.suggest_kind(df[target])
except ValueError as error:
    st.error(str(error))
    st.stop()
kinds = ["logistic", "linear"] if suggested == "logistic" else ["linear"]
kind = st.radio("Model", kinds, horizontal=True, key=f"m_kind_{target}",
                format_func=lambda k: f"{k} regression")
available = modelling.usable_features(df, target)
features = st.multiselect("Features", available, default=modelling.default_features(df, target, available),
                          key=f"m_features_{target}",
                          help="Starts with the six numbers most correlated with the target; change freely.")
if not features:
    st.info("Choose at least one feature.")
    st.stop()

result = fit_cached(df, target, tuple(features), kind)
st.session_state["model"] = result
for note in result.notes:
    st.caption(note)

m = result.metrics
if kind == "logistic":
    c = st.columns(3)
    c[0].metric("Cross-validated AUC", f"{m['cv_auc_mean']:.3f}", help=f"± {m['cv_auc_sd']:.3f} across 5 folds")
    c[1].metric("Test AUC", f"{m['test_auc']:.3f}")
    c[2].metric("Positive rate", f"{m['positive_rate']:.1%}")
    t = st.slider("Decision threshold", 0.05, 0.95, 0.50, 0.01, key="m_threshold")
    tm = modelling.threshold_metrics(result, t)
    st.session_state["threshold"] = tm
    d = st.columns(4)
    d[0].metric("Flagged", tm["flagged"])
    d[1].metric("Precision", f"{tm['precision']:.3f}")
    d[2].metric("Recall", f"{tm['recall']:.3f}")
    d[3].metric("F1", f"{tm['f1']:.3f}")
    st.caption(f"Test set: TP {tm['tp']} · FP {tm['fp']} · FN {tm['fn']} · TN {tm['tn']}")
else:
    c = st.columns(4)
    c[0].metric("Cross-validated R²", f"{m['cv_r2_mean']:.3f}", help=f"± {m['cv_r2_sd']:.3f} across 5 folds")
    c[1].metric("Test R²", f"{m['test_r2']:.3f}")
    c[2].metric("Test MAE", f"{m['test_mae']:,.2f}")
    c[3].metric("Test RMSE", f"{m['test_rmse']:,.2f}")

left, right = st.columns([3, 2])
with left:
    st.image(report.effects_chart_png(result))
with right:
    st.dataframe(result.coefficients.round(3), hide_index=True, width="stretch", height=360)
st.page_link("views/insights.py", label="Next: insights", icon="➡️")
