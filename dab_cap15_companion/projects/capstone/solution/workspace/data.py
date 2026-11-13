"""Page 1: getting data in, from CSV files or SQLite databases, read-only."""
import re
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd

from . import loader

SAMPLES = Path(__file__).resolve().parents[1] / "sample_data"
MAX_ROWS = 200_000


def from_csv(raw: bytes) -> tuple[pd.DataFrame, list[str]]:
    """Read any CSV with Project 1's robust loader; return the data and notes on what was inferred."""
    result = loader.load_csv(raw)
    return result.data, [f"Encoding {result.encoding}, delimiter {result.delimiter!r}"] + result.notes


def db_path_from_bytes(raw: bytes) -> Path:
    """Write an uploaded database to a temporary file so that sqlite3 can open it."""
    if not raw.startswith(b"SQLite format 3\x00"):
        raise ValueError("This file is not a SQLite database.")
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.write(raw)
    tmp.close()
    return Path(tmp.name)


def connect_read_only(path: Path) -> sqlite3.Connection:
    """Open a database so that nothing the app does can change it."""
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def list_tables(path: Path) -> pd.DataFrame:
    with connect_read_only(path) as con:
        names = pd.read_sql("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name", con)["name"]
        counts = [con.execute(f'SELECT COUNT(*) FROM "{n}"').fetchone()[0] for n in names]
    return pd.DataFrame({"table": names, "rows": counts})


SAFE_SQL = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)


def run_select(path: Path, sql: str) -> pd.DataFrame:
    """Run one SELECT (or WITH ... SELECT) statement on a read-only connection."""
    statement = sql.strip().rstrip(";")
    if ";" in statement:
        raise ValueError("Run one statement at a time.")
    if not SAFE_SQL.match(statement):
        raise ValueError("Only SELECT queries are allowed here.")
    with connect_read_only(path) as con:
        df = pd.read_sql(f"SELECT * FROM ({statement}) LIMIT {MAX_ROWS + 1}", con)
    if len(df) > MAX_ROWS:
        raise ValueError(f"The query returns more than {MAX_ROWS:,} rows; add a WHERE clause or aggregate.")
    return df
