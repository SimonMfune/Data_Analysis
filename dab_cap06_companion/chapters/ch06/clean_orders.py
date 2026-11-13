"""clean_orders.py — the Chapter 6 cleaning pipeline for data/raw/kb_orders_messy.csv (Listing 6.20).

Run from the repository root:
    python chapters/ch06/clean_orders.py
It writes chapters/ch06/output/orders_clean.csv and chapters/ch06/output/cleaning_log.csv.
Each step is a small function that takes a DataFrame and a log, and returns a new DataFrame.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "kb_orders_messy.csv"
OUT = Path(__file__).resolve().parent / "output"

PROVINCES = ["Central", "Copperbelt", "Eastern", "Luapula", "Lusaka", "Muchinga",
             "North-Western", "Northern", "Southern", "Western"]
PROVINCE_ALIASES = {"cb": "Copperbelt", "copper belt": "Copperbelt", "lsk": "Lusaka",
                    "nw": "North-Western", "north western": "North-Western",
                    "northwestern": "North-Western"}
CHANNELS = {"web": "Web", "app": "App", "whatsapp": "WhatsApp"}


class CleaningLog:
    """Records what each step changed, so the cleaning can be audited."""

    def __init__(self):
        self.rows = []

    def add(self, step, affected, note):
        self.rows.append({"step": step, "rows_affected": int(affected), "note": note})

    def to_frame(self):
        return pd.DataFrame(self.rows)


def load_raw(path=RAW):
    """Read the export with every column as text, so nothing is silently converted."""
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""])


def strip_text(df, log):
    df = df.copy()
    changed = 0
    for col in df.columns:
        stripped = df[col].str.strip()
        changed += int((stripped != df[col]).fillna(False).sum())
        df[col] = stripped
    log.add("strip_text", changed, "removed leading/trailing spaces in all text columns")
    return df


def drop_exact_duplicates(df, log):
    before = len(df)
    df = df.drop_duplicates()
    log.add("drop_exact_duplicates", before - len(df), "rows identical in every column")
    return df


def standardise_channel(df, log):
    df = df.copy()
    canonical = df["channel"].str.lower().map(CHANNELS)
    changed = (canonical != df["channel"]) & df["channel"].notna()
    df["channel"] = canonical
    log.add("standardise_channel", changed.sum(), "WEB/APP/WHATSAPP -> Web/App/WhatsApp")
    return df


def standardise_province(df, log):
    df = df.copy()
    key = df["province"].str.lower()
    lookup = {p.lower(): p for p in PROVINCES} | PROVINCE_ALIASES
    canonical = key.map(lookup)
    unknown = df["province"].notna() & canonical.isna()
    if unknown.any():
        raise ValueError(f"unmapped provinces: {sorted(df.loc[unknown, 'province'].unique())}")
    changed = (canonical != df["province"]) & df["province"].notna()
    df["province"] = canonical
    log.add("standardise_province", changed.sum(), "case variants and abbreviations -> 10 provinces")
    return df


def drop_near_duplicates(df, log):
    before = len(df)
    df = df.drop_duplicates(subset="order_id", keep="first")
    log.add("drop_near_duplicates", before - len(df), "same order_id after standardising text")
    return df


DATE_FORMATS = {"ISO": "%Y-%m-%d %H:%M:%S", "DD/MM/YYYY": "%d/%m/%Y", "DD Mon YYYY": "%d %b %Y"}


def parse_dates(df, log):
    """Parse each known format explicitly. Never let pandas guess when formats are mixed."""
    df = df.copy()
    parsed = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    counts = {}
    for name, fmt in DATE_FORMATS.items():
        attempt = pd.to_datetime(df["order_date"], format=fmt, errors="coerce")
        new = parsed.isna() & attempt.notna()
        parsed[new] = attempt[new]
        counts[name] = int(new.sum())
    if parsed.isna().any():
        raise ValueError(f"unparsed dates: {df.loc[parsed.isna(), 'order_date'].head().tolist()}")
    df["order_date"] = parsed
    log.add("parse_dates", len(df), ", ".join(f"{k}: {v:,}" for k, v in counts.items()))
    return df


def parse_money(df, log):
    df = df.copy()
    text = df["total"].str.startswith("K").sum()
    df["total_zmw"] = pd.to_numeric(df["total"].str.replace("K", "").str.replace(",", ""))
    df = df.drop(columns="total")
    for col in ["subtotal_zmw", "discount_zmw", "delivery_fee_zmw"]:
        df[col] = pd.to_numeric(df[col])
    df["items"] = pd.to_numeric(df["items"]).astype("Int64")
    log.add("parse_money", text, "'K1,541.48'-style totals -> numbers; other numeric columns cast")
    return df


def normalise_phone(df, log):
    df = df.copy()
    digits = df["customer_phone"].str.replace(r"\D", "", regex=True)
    national = digits.str.replace(r"^(260|0)", "", regex=True)     # drop country code or trunk 0
    valid = national.str.fullmatch(r"[79]\d{8}")
    df["customer_phone"] = ("+260" + national).where(valid)
    log.add("normalise_phone", valid.sum(), "four formats -> +260XXXXXXXXX")
    return df


def fix_negative_items(df, log):
    df = df.copy()
    neg = df["items"] < 0
    df.loc[neg, "items"] = -df.loc[neg, "items"]
    log.add("fix_negative_items", neg.sum(), "negative item counts made positive (sign error)")
    return df


def fill_delivery_fee(df, log):
    """total = subtotal - discount + fee, so a missing fee can be derived exactly."""
    df = df.copy()
    miss = df["delivery_fee_zmw"].isna()
    derived = (df["total_zmw"] - df["subtotal_zmw"] + df["discount_zmw"]).round(2)
    df.loc[miss, "delivery_fee_zmw"] = derived[miss]
    log.add("fill_delivery_fee", miss.sum(), "derived from total - subtotal + discount")
    return df


def fix_decimal_shift(df, log):
    """Subtotals 100 times too large break the total identity; rebuild them from it."""
    df = df.copy()
    implied = (df["total_zmw"] + df["discount_zmw"] - df["delivery_fee_zmw"]).round(2)
    shifted = (df["subtotal_zmw"] - implied).abs() > 0.01
    df.loc[shifted, "subtotal_zmw"] = implied[shifted]
    log.add("fix_decimal_shift", shifted.sum(), "subtotal rebuilt where it broke the total identity")
    return df


def fill_from_customer(df, log, column):
    """Fill a missing value from the same customer's other orders, where they agree."""
    df = df.copy()
    known = df.dropna(subset=[column]).groupby("customer_id")[column].agg(
        lambda s: s.mode().iat[0] if s.nunique() == 1 else pd.NA)
    miss = df[column].isna()
    df.loc[miss, column] = df.loc[miss, "customer_id"].map(known)
    filled = miss.sum() - df[column].isna().sum()
    log.add(f"fill_{column}", filled, f"from the customer's other orders ({df[column].isna().sum()} still missing)")
    return df


def fill_channel_unknown(df, log):
    df = df.copy()
    miss = df["channel"].isna()
    df["channel"] = df["channel"].fillna("Unknown")
    log.add("fill_channel_unknown", miss.sum(), "missing channel cannot be derived -> 'Unknown'")
    return df


def set_categories(df, log):
    df = df.copy()
    df["province"] = pd.Categorical(df["province"], categories=PROVINCES)
    for col in ["channel", "delivery_method", "payment_method", "status"]:
        df[col] = df[col].astype("category")
    log.add("set_categories", len(df), "repeated text columns stored as category")
    return df


def validate(df):
    """Raise AssertionError if any rule is broken; return the DataFrame unchanged otherwise."""
    assert df["order_id"].is_unique, "duplicate order_id"
    assert df["order_date"].between("2023-01-01", "2026-01-01").all(), "date out of range"
    assert df["province"].dropna().isin(PROVINCES).all(), "unknown province"
    assert df["channel"].isin(list(CHANNELS.values()) + ["Unknown"]).all(), "unknown channel"
    assert (df["items"] > 0).all(), "non-positive item count"
    identity = (df["subtotal_zmw"] - df["discount_zmw"] + df["delivery_fee_zmw"] - df["total_zmw"]).abs()
    assert (identity <= 0.01).all(), "total does not reconcile"
    assert df["customer_phone"].dropna().str.fullmatch(r"\+260[79]\d{8}").all(), "bad phone format"
    return df


def clean(path=RAW):
    log = CleaningLog()
    df = (load_raw(path)
          .pipe(strip_text, log)
          .pipe(drop_exact_duplicates, log)
          .pipe(standardise_channel, log)
          .pipe(standardise_province, log)
          .pipe(drop_near_duplicates, log)
          .pipe(parse_dates, log)
          .pipe(parse_money, log)
          .pipe(normalise_phone, log)
          .pipe(fix_negative_items, log)
          .pipe(fill_delivery_fee, log)
          .pipe(fix_decimal_shift, log)
          .pipe(fill_from_customer, log, "province")
          .pipe(fill_from_customer, log, "customer_phone")
          .pipe(fill_channel_unknown, log)
          .pipe(set_categories, log)
          .pipe(validate))
    return df.sort_values("order_date").reset_index(drop=True), log.to_frame()


if __name__ == "__main__":
    orders, log = clean()
    OUT.mkdir(exist_ok=True)
    orders.to_csv(OUT / "orders_clean.csv", index=False)
    log.to_csv(OUT / "cleaning_log.csv", index=False)
    print(log.to_string(index=False))
    print(f"\n{len(orders):,} clean orders written to {OUT.relative_to(ROOT) / 'orders_clean.csv'}")
