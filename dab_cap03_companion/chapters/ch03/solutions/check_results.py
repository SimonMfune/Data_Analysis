"""Chapter 3 — independent check of every expected result, in pandas.

Cleans data/raw/kb_raw_transactions.xlsx the same way the chapter's Excel
formulas do, then prints the control totals, Table 3.4 and Table 3.5.
Run from the repository root:  python chapters/ch03/solutions/check_results.py
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data" / "raw" / "kb_raw_transactions.xlsx"
PAY = {"airtelmoney": "Airtel Money", "mtnmomo": "MTN MoMo", "zamtelkwacha": "Zamtel Kwacha",
       "card": "Card", "cashondelivery": "Cash on Delivery"}


def excel_trim(s):
    """TRIM: strip spaces at both ends and collapse internal runs to one space."""
    return re.sub(r" +", " ", str(s).strip(" "))


def excel_proper(s):
    """PROPER: capitalise the first letter after any non-letter (so Ng'andu -> Ng'Andu)."""
    return re.sub(r"[A-Za-z]+", lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(), s)


def clean(path=SRC):
    sheets = pd.read_excel(path, sheet_name=None)
    t, products = sheets["Transactions"], sheets["Products"]
    d = t.drop_duplicates().copy()
    d["Province Clean"] = d["Province"].map(lambda s: excel_proper(excel_trim(s)))
    d["Category Clean"] = d["Category"].map(lambda s: excel_proper(excel_trim(s)))
    d["Customer Clean"] = d["Customer Name"].map(lambda s: excel_proper(excel_trim(s)).replace("Ng'A", "Ng'a"))
    d["Payment Clean"] = d["Payment Method"].map(lambda s: PAY.get(s.replace(" ", "").lower(), "Unknown"))
    d["Price Clean"] = d["Unit Price"].map(lambda v: float(str(v).replace("K", "").replace(",", "")))
    d["Line Total"] = d["Qty"] * d["Price Clean"]
    d["Unit Cost"] = d["Product ID"].map(products.set_index("Product ID")["Unit Cost (ZMW)"])
    d["Gross Margin"] = (d["Price Clean"] - d["Unit Cost"]) * d["Qty"]
    d["Month"] = d["Date"].dt.strftime("%Y-%m")
    d["Quarter"] = "Qtr" + d["Date"].dt.quarter.astype(str)
    d["Size Band"] = pd.cut(d["Line Total"], [-1, 499.999, 4999.999, 1e12], labels=["Small", "Medium", "Large"])
    return t, d


def main():
    raw, d = clean()
    print(f"Raw rows {len(raw):,}; after Remove Duplicates {len(d):,} ({len(raw) - len(d)} removed)")
    print(f"Control total (Line Total): K{d['Line Total'].sum():,.2f}")
    print(f"Gross margin: K{d['Gross Margin'].sum():,.2f} ({d['Gross Margin'].sum() / d['Line Total'].sum():.1%})")
    print(f"Size bands: {d['Size Band'].value_counts().to_dict()}")
    print(f"Distinct customer names: {d['Customer Clean'].nunique():,}\n")
    s = d.groupby("Province Clean").agg(Revenue=("Line Total", "sum"), Lines=("Line Total", "size"),
                                        Average=("Line Total", "mean"), Margin=("Gross Margin", "sum"))
    s["Margin %"] = (s["Margin"] / s["Revenue"] * 100).round(1)
    print("Table 3.4\n", s.sort_values("Revenue", ascending=False).round(2).to_string(), "\n")
    pv = d.pivot_table(index="Province Clean", columns="Quarter", values="Line Total", aggfunc="sum",
                       margins=True, margins_name="Grand Total").round(0)
    print("Table 3.5\n", pv.sort_values("Grand Total", ascending=False).to_string())


if __name__ == "__main__":
    main()
