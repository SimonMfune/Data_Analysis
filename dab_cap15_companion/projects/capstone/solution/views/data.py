"""Page 1, Data: load a CSV file, a SQLite database (whole table or a SELECT query), or a sample."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the app folder

import streamlit as st  # noqa: E402

from workspace import data  # noqa: E402

st.title("📥 Data")
st.write("Bring in the data to analyse. Databases are opened read-only.")


@st.cache_data(show_spinner="Reading...")
def read_csv(raw: bytes):
    return data.from_csv(raw)


@st.cache_data(show_spinner="Querying...")
def query(path: str, sql: str):
    return data.run_select(Path(path), sql)


def use(name, df, notes):
    st.session_state["dataset"] = {"name": name, "df": df, "notes": notes}
    for key in ["prepared", "model", "insights"]:          # later steps belong to the old data
        st.session_state.pop(key, None)


source = st.radio("Source", ["Sample: Kwacha Basket database", "Sample: fintech loans CSV",
                             "Upload a CSV file", "Upload a SQLite database"], key="data_source")
db_path = None
if source == "Sample: Kwacha Basket database":
    db_path = data.SAMPLES / "kwacha_basket_sample.db"
elif source == "Sample: fintech loans CSV":
    if st.button("Load fintech_loans.csv", type="primary"):
        df, notes = read_csv((data.SAMPLES / "fintech_loans.csv").read_bytes())
        use("fintech_loans.csv", df, notes)
elif source == "Upload a CSV file":
    up = st.file_uploader("CSV file", type=["csv", "txt"])
    if up is not None and st.button("Load file", type="primary"):
        try:
            df, notes = read_csv(up.getvalue())
            use(up.name, df, notes)
        except Exception as error:
            st.error(f"{up.name} could not be read: {error}")
else:
    up = st.file_uploader("SQLite database", type=["db", "sqlite", "sqlite3"])
    if up is not None:
        try:
            db_path = data.db_path_from_bytes(up.getvalue())
        except ValueError as error:
            st.error(str(error))

if db_path is not None:
    tables = data.list_tables(db_path)
    st.dataframe(tables, hide_index=True)
    table = st.selectbox("Table", tables["table"], key="data_table")
    sql = st.text_area("SQL (one SELECT statement)", f"SELECT * FROM {table}", key=f"sql_{table}")
    if st.button("Run query and use the result", type="primary"):
        try:
            use(f"{db_path.stem}: {table}", query(str(db_path), sql), [f"SQL: {sql}"])
        except Exception as error:
            st.error(str(error))

if "dataset" in st.session_state:
    ds = st.session_state["dataset"]
    st.success(f"Using **{ds['name']}**: {len(ds['df']):,} rows, {ds['df'].shape[1]} columns.")
    st.dataframe(ds["df"].head(8), width="stretch")
    with st.expander("How the data was read"):
        st.write("\n".join(f"- {n}" for n in ds["notes"]))
    st.page_link("views/prepare.py", label="Next: prepare the data", icon="➡️")
