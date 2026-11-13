"""run_sql.py — run SQL against the Kwacha Basket database and print the results.

Usage (from the repository root):
    python chapters/ch04/run_sql.py chapters/ch04/listings/04_01_first_look.sql
    python chapters/ch04/run_sql.py -q "SELECT COUNT(*) FROM orders;"
    python chapters/ch04/run_sql.py --max-rows 50 my_query.sql

Every statement in the file is run in order; the results of each SELECT are printed.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "kwacha_basket.db"


def decimals(values):
    """Decimal places needed to show every float in a column exactly (max 4)."""
    d = 0
    for v in values:
        if isinstance(v, float):
            text = f"{v:.4f}".rstrip("0")
            d = max(d, len(text.split(".")[1]) if "." in text else 0)
    return d


def fmt(v, d):
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return f"{v:.{d}f}"
    return str(v)


def show(cur, max_rows):
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    dec = [decimals(r[i] for r in rows) for i in range(len(cols))]
    dec = [max(d, 2) if d and c.endswith("_zmw") else d for d, c in zip(dec, cols)]  # money: 2 dp
    shown = [[fmt(v, dec[i]) for i, v in enumerate(r)] for r in rows[:max_rows]]
    widths = [max([len(c)] + [len(r[i]) for r in shown]) for i, c in enumerate(cols)]
    num = [all(isinstance(r[i], (int, float)) or r[i] is None for r in rows) and rows for i in range(len(cols))]
    line = lambda vals: "  ".join(v.rjust(w) if n else v.ljust(w) for v, w, n in zip(vals, widths, num)).rstrip()
    print(line(cols))
    print("  ".join("-" * w for w in widths))
    for r in shown:
        print(line(r))
    extra = f" (first {max_rows} shown)" if len(rows) > max_rows else ""
    print(f"({len(rows)} row{'s' if len(rows) != 1 else ''}{extra})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("-q", "--query")
    ap.add_argument("--max-rows", type=int, default=20)
    a = ap.parse_args()
    sql = a.query if a.query else Path(a.file).read_text(encoding="utf-8")
    con = sqlite3.connect(DB)
    statements = [s for s in sqlite3_split(sql) if s.strip()]
    for i, stmt in enumerate(statements):
        cur = con.execute(stmt)
        if cur.description:
            if i:
                print()
            show(cur, a.max_rows)
    con.close()


def sqlite3_split(sql):
    """Split a script into complete statements (handles semicolons inside strings)."""
    buf, out = "", []
    for line in sql.splitlines(keepends=True):
        if line.strip().startswith("--") and not buf.strip():
            continue
        buf += line
        if sqlite3.complete_statement(buf):
            out.append(buf)
            buf = ""
    if buf.strip():
        out.append(buf)
    return out


if __name__ == "__main__":
    sys.exit(main())
