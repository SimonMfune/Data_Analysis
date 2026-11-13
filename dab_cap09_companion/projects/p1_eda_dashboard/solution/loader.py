"""Milestone M1: read any CSV file robustly.

Every column is read as text first, so that nothing is lost or guessed silently.
`infer_types` then converts each column deliberately and records what it did.
"""
import csv
import io
from dataclasses import dataclass, field

import pandas as pd

ENCODINGS = ["utf-8-sig", "cp1252", "latin-1"]        # latin-1 can decode any byte
DELIMITERS = ",;\t|"
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%Y-%m-%d %H:%M:%S"]
TRUE_FALSE = {frozenset({"yes", "no"}), frozenset({"y", "n"}), frozenset({"true", "false"})}


@dataclass
class LoadResult:
    data: pd.DataFrame
    encoding: str
    delimiter: str
    notes: list = field(default_factory=list)


def decode(raw: bytes) -> tuple[str, str]:
    """Return the text and the first encoding in ENCODINGS that decodes it without error."""
    for encoding in ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("The file could not be decoded")     # unreachable: latin-1 never fails


def sniff_delimiter(text: str) -> str:
    """Guess the delimiter from the first lines; fall back to a comma."""
    sample = "\n".join(text.splitlines()[:50])
    try:
        return csv.Sniffer().sniff(sample, delimiters=DELIMITERS).delimiter
    except csv.Error:
        return ","


def to_number(series: pd.Series) -> pd.Series:
    """Convert text such as 'K1,250.50' or ' 300 ' to numbers; unparseable values become NaN."""
    cleaned = (series.str.strip()
               .str.replace(r"^(ZMW|K)\s*", "", regex=True)
               .str.replace(",", "", regex=False))
    return pd.to_numeric(cleaned, errors="coerce")


def to_date(series: pd.Series) -> tuple[pd.Series | None, str | None]:
    """Try each explicit date format in turn; return the parsed column and the format, or None.

    Formats are tried one at a time on purpose. Chapter 6 showed that `format="mixed"`
    with `dayfirst=True` silently swaps day and month in ISO dates.
    """
    values = series.dropna()
    for fmt in DATE_FORMATS:
        parsed = pd.to_datetime(values, format=fmt, errors="coerce")
        if len(values) and parsed.notna().mean() >= 0.95:
            return pd.to_datetime(series, format=fmt, errors="coerce"), fmt
    return None, None


def infer_types(df: pd.DataFrame, threshold: float = 0.95) -> tuple[pd.DataFrame, list[str]]:
    """Convert text columns to numbers, dates or yes/no flags where at least `threshold`
    of the non-missing values agree. Returns the new DataFrame and a list of notes."""
    out, notes = df.copy(), []
    for col in out.columns:
        s = out[col]
        present = s.dropna()
        if present.empty:
            notes.append(f"{col}: empty column, left as text")
            continue
        number = to_number(present)
        if number.notna().mean() >= threshold:
            out[col] = to_number(s)
            lost = int(out[col].isna().sum() - s.isna().sum())
            notes.append(f"{col}: number" + (f" ({lost} unparseable value(s) set to missing)" if lost else ""))
            continue
        parsed, fmt = to_date(s)
        if parsed is not None:
            out[col] = parsed
            notes.append(f"{col}: date, format {fmt}")
            continue
        if frozenset(present.str.strip().str.lower().unique()) in TRUE_FALSE:
            out[col] = out[col].str.strip().str.title().astype("category")
            notes.append(f"{col}: yes/no flag")
            continue
        if present.nunique() <= max(20, len(present) * 0.05) and present.nunique() < len(present):
            out[col] = out[col].astype("category")
            notes.append(f"{col}: category ({present.nunique()} values)")
    return out, notes


def load_csv(raw: bytes) -> LoadResult:
    """Decode, sniff the delimiter, read everything as text, then infer types."""
    text, encoding = decode(raw)
    delimiter = sniff_delimiter(text)
    df = pd.read_csv(io.StringIO(text), sep=delimiter, dtype=str,
                     keep_default_na=False, na_values=[""])
    df.columns = [str(c).strip() for c in df.columns]
    df, notes = infer_types(df)
    return LoadResult(df, encoding, delimiter, notes)
