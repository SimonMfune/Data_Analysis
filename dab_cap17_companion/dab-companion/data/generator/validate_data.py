"""
Validates the frozen Kwacha Basket dataset and writes data/DATA_QA.md.

Run from the repository root:  python data/generator/validate_data.py
Checks integrity (keys, totals), reproducibility (seed 2026) and that the
business patterns each chapter relies on are present in the data.
"""
from __future__ import annotations

import hashlib
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1]
results: list[tuple[str, str, bool]] = []


def check(name, value, ok):
    results.append((name, str(value), bool(ok)))


def q(con, sql):
    return con.execute(sql).fetchone()[0]


def main():
    con = sqlite3.connect(DATA / "kwacha_basket.db")
    # ---------------- integrity
    counts = {t: q(con, f"SELECT COUNT(*) FROM {t}") for t in
              ["customers", "products", "suppliers", "orders", "order_items", "payments",
               "deliveries", "returns", "campaigns", "reviews"]}
    check("Row counts", ", ".join(f"{k} {v:,}" for k, v in counts.items()), counts["orders"] > 50000)
    orphans = sum(q(con, s) for s in [
        "SELECT COUNT(*) FROM orders o LEFT JOIN customers c USING(customer_id) WHERE c.customer_id IS NULL",
        "SELECT COUNT(*) FROM order_items i LEFT JOIN orders o USING(order_id) WHERE o.order_id IS NULL",
        "SELECT COUNT(*) FROM order_items i LEFT JOIN products p USING(product_id) WHERE p.product_id IS NULL",
        "SELECT COUNT(*) FROM payments p LEFT JOIN orders o USING(order_id) WHERE o.order_id IS NULL",
        "SELECT COUNT(*) FROM products p LEFT JOIN suppliers s USING(supplier_id) WHERE s.supplier_id IS NULL",
        "SELECT COUNT(*) FROM orders o LEFT JOIN campaigns c USING(campaign_id) WHERE o.campaign_id IS NOT NULL AND c.campaign_id IS NULL"])
    check("Foreign-key orphans", orphans, orphans == 0)
    bad = q(con, """SELECT COUNT(*) FROM orders o JOIN payments p USING(order_id)
                    JOIN (SELECT order_id, SUM(quantity*unit_price_zmw) s FROM order_items GROUP BY order_id) i USING(order_id)
                    WHERE ABS(p.amount_zmw - (i.s - o.discount_zmw + o.delivery_fee_zmw)) > 0.02""")
    check("Payment amount = items - discount + delivery fee", f"{bad} mismatches", bad == 0)
    early = q(con, "SELECT COUNT(*) FROM orders o JOIN customers c USING(customer_id) WHERE substr(o.order_datetime,1,10) < c.signup_date")
    check("No order before customer signup", early, early == 0)
    rng_dates = con.execute("SELECT MIN(order_datetime), MAX(order_datetime) FROM orders").fetchone()
    check("Order date range", f"{rng_dates[0]} to {rng_dates[1]}", rng_dates[0] >= "2023-01-01" and rng_dates[1] <= "2025-12-31 23:59:59")

    # ---------------- patterns
    o = pd.read_sql("SELECT order_id, customer_id, order_datetime, province, campaign_id, status FROM orders", con,
                    parse_dates=["order_datetime"])
    o = o[o.status != "Cancelled"]
    yr = o.order_datetime.dt.year.value_counts().sort_index()
    check("Year-on-year order growth", " / ".join(f"{y}: {n:,}" for y, n in yr.items()), yr.is_monotonic_increasing)
    o25 = o[o.order_datetime.dt.year == 2025]
    by_m = o25.groupby(o25.order_datetime.dt.month).size()
    dec = by_m[12] / by_m.drop(12).mean()
    check("December festive peak (2025, vs other-month mean)", f"x{dec:.2f}", dec > 1.3)
    day = o.order_datetime.dt.day
    payday = day.isin([25, 26, 27, 28, 29, 30, 31, 1, 2])
    days_in = pd.Series(pd.date_range("2023-01-01", "2025-12-31")).dt.day
    pd_days = days_in.isin([25, 26, 27, 28, 29, 30, 31, 1, 2])
    ratio = (payday.sum() / pd_days.sum()) / ((~payday).sum() / (~pd_days).sum())
    check("Month-end payday effect (orders per day)", f"x{ratio:.2f}", ratio > 1.15)
    it = pd.read_sql("""SELECT o.order_datetime, o.province, p.category FROM order_items i
                        JOIN orders o USING(order_id) JOIN products p USING(product_id)""", con, parse_dates=["order_datetime"])
    st = it.assign(m=it.order_datetime.dt.month).groupby("m").category.apply(lambda s: (s == "Stationery").mean())
    term = st[[1, 5, 9]].mean() / st.drop([1, 5, 9]).mean()
    check("School-term stationery effect (Jan/May/Sep share vs other months)", f"x{term:.2f}", term > 1.5)
    el = it.groupby("province").category.apply(lambda s: (s == "Electronics").mean())
    check("Copperbelt electronics share vs Lusaka", f"{el['Copperbelt']:.1%} vs {el['Lusaka']:.1%}", el["Copperbelt"] > el["Lusaka"])
    d = pd.read_csv(DATA / "clean" / "kb_delivery_times.csv")
    late = d.groupby("province").delayed_flag.mean()
    check("Late deliveries: Lusaka vs Western", f"{late['Lusaka']:.1%} vs {late['Western']:.1%} (overall {d.delayed_flag.mean():.1%})",
          late["Western"] > late["Lusaka"])
    camp = pd.read_sql("SELECT start_date, end_date FROM campaigns", con, parse_dates=["start_date", "end_date"])
    od = o.order_datetime.dt.normalize()
    in_c = np.zeros(len(od), bool)
    all_days = pd.Series(pd.date_range("2023-01-01", "2025-12-31"))
    day_c = np.zeros(len(all_days), bool)
    for s, e in camp.itertuples(index=False):
        in_c |= ((od >= s) & (od <= e)).to_numpy()
        day_c |= ((all_days >= s) & (all_days <= e)).to_numpy()
    # compare within-month: campaign days vs non-campaign days, same months
    pay_o = od.dt.day.isin([25, 26, 27, 28, 29, 30, 31, 1, 2]).to_numpy()
    pay_d = all_days.dt.day.isin([25, 26, 27, 28, 29, 30, 31, 1, 2]).to_numpy()
    om = pd.DataFrame({"month": od.dt.to_period("M"), "camp": in_c})[~pay_o]
    per_day = om.groupby(["month", "camp"]).size()
    dm = pd.DataFrame({"month": all_days.dt.to_period("M"), "camp": day_c})[~pay_d].groupby(["month", "camp"]).size()
    rate = (per_day / dm).unstack()
    uplift = (rate[True] / rate[False]).median()
    check("Campaign uplift (median within-month ratio, non-payday days)", f"x{uplift:.2f}", 1.0 < uplift < 1.3)

    # ---------------- chapter files
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.metrics import r2_score, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    pr = pd.read_csv(DATA / "clean" / "kb_product_pricing.csv")
    X, y = pr[["category", "brand_tier", "imported_flag", "weight_kg", "unit_cost_zmw"]], pr.list_price_zmw
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=2026)
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["category", "brand_tier"])], remainder="passthrough")
    m = make_pipeline(pre, LinearRegression()).fit(Xtr, ytr)
    r2 = r2_score(yte, m.predict(Xte))
    check("Ch 11 pricing regression, test R²", f"{r2:.3f}", 0.85 < r2 < 0.99)
    ch = pd.read_csv(DATA / "clean" / "kb_customer_churn.csv")
    num = ["tenure_days", "age", "orders_total", "orders_last_90d", "orders_last_180d", "spend_last_180d_zmw",
           "avg_basket_zmw", "recency_days", "pct_orders_delayed", "returns_count", "app_share"]
    Xtr, Xte, ytr, yte = train_test_split(ch[num], ch.churned, test_size=0.25, stratify=ch.churned, random_state=2026)
    lg = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
    auc = roc_auc_score(yte, lg.predict_proba(Xte)[:, 1])
    check("Ch 12 churn: rows / positive rate / baseline AUC", f"{len(ch):,} / {ch.churned.mean():.1%} / {auc:.3f}",
          0.12 < ch.churned.mean() < 0.30 and 0.65 < auc < 0.95)
    ab = pd.read_csv(DATA / "clean" / "kb_campaign_ab.csv")
    cr = ab.groupby("group").converted.mean()
    check("Ch 10 A/B conversion WhatsApp vs SMS", f"{cr['WhatsApp']:.2%} vs {cr['SMS']:.2%}", cr["WhatsApp"] > cr["SMS"])
    messy = pd.read_csv(DATA / "raw" / "kb_orders_messy.csv")
    check("Ch 6 messy file: rows / exact duplicates", f"{len(messy):,} / {messy.duplicated().sum()}", messy.duplicated().sum() == 150)
    x = pd.read_excel(DATA / "raw" / "kb_raw_transactions.xlsx", sheet_name=None)
    check("Ch 3 workbook sheets / transaction rows", f"{list(x)} / {len(x['Transactions']):,}", len(x["Transactions"]) == 2500)
    un = [pd.read_csv(DATA / "unseen" / "fintech_loans.csv"),
          pd.read_csv(DATA / "unseen" / "clinic_visits.csv", sep=";"),
          pd.read_csv(DATA / "unseen" / "marketing_leads.csv", encoding="latin-1")]
    check("Unseen CSVs load with correct options", " / ".join(f"{len(u)}x{u.shape[1]}" for u in un), all(u.shape[1] > 5 for u in un))

    # ---------------- reproducibility
    def same(a, b):
        x, y = pd.read_csv(a, dtype=str, keep_default_na=False), pd.read_csv(b, dtype=str, keep_default_na=False)
        if x.shape != y.shape or list(x.columns) != list(y.columns):
            return False
        for c in x.columns:
            if (x[c] == y[c]).all():
                continue
            xn, yn = pd.to_numeric(x[c], errors="coerce"), pd.to_numeric(y[c], errors="coerce")
            if xn.isna().ne(yn.isna()).any() or (xn - yn).abs().max() > 0.011:
                return False
        return True
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, str(DATA / "generator" / "generate_data.py"), "--out", tmp],
                       check=True, capture_output=True)
        files = sorted((DATA / "clean").glob("*.csv")) + sorted((DATA / "raw").glob("*.csv"))
        exact = sum(f.read_bytes() == (Path(tmp) / f.parent.name / f.name).read_bytes() for f in files)
        diffs = [f.name for f in files if not same(f, Path(tmp) / f.parent.name / f.name)]
    check("Reproducible from seed 2026 (values match to K0.01 on regeneration)",
          f"{exact}/{len(files)} files byte-identical; all values match" if not diffs else diffs, not diffs)

    # ---------------- report
    lines = ["# Kwacha Basket dataset — validation report", "",
             "Generated by `data/generator/validate_data.py`. Every check must pass before a chapter is drafted against the data.", "",
             "| Check | Result | Status |", "|---|---|---|"]
    lines += [f"| {n} | {v} | {'PASS' if ok else 'FAIL'} |" for n, v, ok in results]
    (DATA / "DATA_QA.md").write_text("\n".join(lines) + "\n")
    for n, v, ok in results:
        print(("PASS " if ok else "FAIL ") + n + ": " + v)
    sys.exit(0 if all(ok for *_, ok in results) else 1)


if __name__ == "__main__":
    main()
