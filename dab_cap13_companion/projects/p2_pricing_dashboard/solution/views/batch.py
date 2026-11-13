"""Milestone M5: price many products at once from a CSV file, after checking it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import common  # noqa: E402
import serving  # noqa: E402
from features import FEATURES  # noqa: E402
from validation import validate_batch  # noqa: E402

artefact = common.start_page()
SAMPLES = Path(__file__).resolve().parents[1] / "sample_data"
st.title("Batch scoring")
st.write(f"Upload a CSV with the columns **{', '.join(FEATURES)}**. Other columns, such as a "
         "product name, are kept. Rows with problems are listed and left out.")

uploaded = st.file_uploader("CSV file", type=["csv"])
sample = None
if uploaded is None:
    sample = st.selectbox("...or try a sample", ["(none)"] + sorted(p.name for p in SAMPLES.glob("*.csv")),
                          key="batch_sample")
if uploaded is not None:
    name, source = uploaded.name, uploaded
elif sample and sample != "(none)":
    name, source = sample, SAMPLES / sample
else:
    st.stop()

try:
    raw = pd.read_csv(source)
except Exception as error:
    st.error(f"{name} could not be read as a CSV file ({error.__class__.__name__}). "
             "Save it from Excel as 'CSV UTF-8' and try again.")
    st.stop()

good, problems = validate_batch(raw)
if problems:
    st.error(f"{len(problems)} problem(s) found in {name}. "
             f"{len(good)} of {len(raw)} rows can be priced.")
    st.dataframe(pd.DataFrame({"Problem": problems}), hide_index=True, width="stretch")
if good.empty:
    st.stop()

scored = serving.suggest(artefact, good)
st.success(f"Priced {len(scored)} product(s).")
st.caption(common.typical_error_caption(artefact))
show = [c for c in scored.columns if c not in FEATURES or c in ("category", "unit_cost_zmw")]
st.dataframe(scored[show], hide_index=True, width="stretch")
st.download_button("Download suggestions (CSV)", scored.to_csv(index=False).encode("utf-8"),
                   file_name=f"{Path(name).stem}_suggested.csv", mime="text/csv")
