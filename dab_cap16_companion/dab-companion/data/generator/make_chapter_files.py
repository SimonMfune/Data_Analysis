"""
Builds the chapter teaching files from the Kwacha Basket core tables.

Called by generate_data.py. Files with planted defects go to data/raw/,
analysis-ready files to data/clean/, and Project 1 test files to data/unseen/.
Returns an answer key (dict) that records every planted defect.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

AGE_BINS = [0, 24, 34, 44, 54, 200]
AGE_LABELS = ["18-24", "25-34", "35-44", "45-54", "55+"]
END = pd.Timestamp("2025-12-31 23:59:59")
SNAPSHOT = pd.Timestamp("2025-09-30 23:59:59")
SLA = {"Lusaka": 24, "Copperbelt": 48, "Southern": 72, "Central": 48, "Eastern": 96,
       "Northern": 120, "Muchinga": 120, "Luapula": 120, "North-Western": 96, "Western": 120}


def _order_facts(t):
    items = t["order_items"].merge(t["products"][["product_id", "category", "unit_cost_zmw",
                                                   "list_price_zmw"]], on="product_id")
    items["line_total_zmw"] = (items.quantity * items.unit_price_zmw).round(2)
    infl = items.unit_price_zmw / items.list_price_zmw
    items["line_cost_zmw"] = (items.quantity * items.unit_cost_zmw * infl).round(2)
    o = t["orders"].copy()
    o["order_dt"] = pd.to_datetime(o.order_datetime)
    agg = items.groupby("order_id").agg(items=("quantity", "sum"), subtotal_zmw=("line_total_zmw", "sum"))
    o = o.join(agg, on="order_id")
    o["subtotal_zmw"] = o.subtotal_zmw.round(2)
    o["total_zmw"] = (o.subtotal_zmw - o.discount_zmw + o.delivery_fee_zmw).round(2)
    o = o.merge(t["payments"][["order_id", "method"]], on="order_id")
    return o, items


def _kwacha(x):
    return f"K{x:,.2f}"


def make_all(t, hidden, out: Path, seed: int) -> dict:
    rng = np.random.default_rng(seed + 1)
    raw, clean, unseen = out / "raw", out / "clean", out / "unseen"
    for p in (raw, clean, unseen):
        p.mkdir(parents=True, exist_ok=True)
    key: dict = {"seed": seed}
    o, items = _order_facts(t)
    ok = o[o.status != "Cancelled"]
    cust = t["customers"].copy()
    cust["age"] = 2025 - cust.birth_year
    rev = t["reviews"].merge(o[["order_id", "customer_id"]], on="order_id")

    # ------------------------------------------------------------------ Ch 1
    per = ok.groupby("customer_id").agg(total_orders=("order_id", "count"),
                                        total_spend_zmw=("total_zmw", "sum"))
    pref_pay = ok.groupby("customer_id").method.agg(lambda s: s.mode().iat[0])
    app_users = set(o.customer_id[o.channel == "App"])
    last_rev = rev.sort_values("review_date", kind="stable").groupby("customer_id").review_text.last()
    avg_rating = rev.groupby("customer_id").rating.mean()
    c1 = cust.join(per, on="customer_id", how="inner").sample(200, random_state=seed)
    c1["avg_basket_zmw"] = (c1.total_spend_zmw / c1.total_orders).round(2)
    c1["total_spend_zmw"] = c1.total_spend_zmw.round(2)
    c1["preferred_payment"] = c1.customer_id.map(pref_pay)
    base = c1.customer_id.map(avg_rating)
    sat = np.where(base.notna(), base.round(), rng.choice([2, 3, 4, 5], len(c1), p=[.1, .25, .4, .25]))
    c1["satisfaction_rating"] = np.clip(sat + rng.choice([-1, 0, 0, 0, 1], len(c1)), 1, 5).astype(int)
    c1["nps_score"] = np.clip(np.round(c1.satisfaction_rating * 2 - 1 + rng.normal(0, 1.2, len(c1))), 0, 10).astype(int)
    c1["has_app"] = c1.customer_id.isin(app_users)
    c1["last_review_text"] = c1.customer_id.map(last_rev)
    cols1 = ["customer_id", "first_name", "last_name", "gender", "birth_year", "age", "province",
             "town", "phone", "signup_date", "signup_channel", "loyalty_tier", "total_orders",
             "total_spend_zmw", "avg_basket_zmw", "preferred_payment", "satisfaction_rating",
             "nps_score", "has_app", "last_review_text"]
    c1[cols1].to_csv(clean / "kb_customers_sample.csv", index=False)

    # ------------------------------------------------------------------ Ch 3
    x = items.merge(o[["order_id", "order_dt", "customer_id", "province", "method", "status"]], on="order_id")
    x = x[(x.status != "Cancelled") & (x.order_dt.dt.year == 2025)].sample(2440, random_state=seed)
    x = x.merge(cust[["customer_id", "first_name", "last_name"]], on="customer_id") \
         .merge(t["products"][["product_id", "product_name"]], on="product_id")
    x = x.sort_values("order_dt", kind="stable").reset_index(drop=True)
    tx = pd.DataFrame({
        "Transaction ID": x.order_id + "-" + x.line_no.astype(str),
        "Date": x.order_dt.dt.normalize(),
        "Customer Name": x.first_name + " " + x.last_name,
        "Province": x.province, "Product ID": x.product_id, "Product": x.product_name,
        "Category": x.category, "Qty": x.quantity, "Unit Price": x.unit_price_zmw.astype(object),
        "Payment Method": x.method})
    n = len(tx)
    k3 = {}
    m = rng.random(n) < 0.12
    tx.loc[m, "Province"] = [rng.choice([p.lower(), p.upper(), f" {p}", f"{p} "]) for p in tx.Province[m]]
    k3["province_variants_rows"] = int(m.sum())
    m = rng.random(n) < 0.07
    tx.loc[m, "Category"] = [rng.choice([c.lower(), c.upper(), f"{c} "]) for c in tx.Category[m]]
    k3["category_variants_rows"] = int(m.sum())
    m = rng.random(n) < 0.10
    tx.loc[m, "Customer Name"] = [rng.choice([s.upper(), s.lower(), f"  {s}", s.replace(" ", "  ")])
                                  for s in tx["Customer Name"][m]]
    k3["name_whitespace_or_case_rows"] = int(m.sum())
    m = rng.random(n) < 0.25
    tx.loc[m, "Unit Price"] = [_kwacha(v) for v in x.unit_price_zmw[m]]
    k3["price_as_text_rows"] = int(m.sum())
    m = rng.random(n) < 0.06
    tx.loc[m, "Payment Method"] = [rng.choice([p.upper(), p.lower(), p.replace(" ", "")]) for p in tx["Payment Method"][m]]
    k3["payment_variants_rows"] = int(m.sum())
    dup = tx.sample(60, random_state=seed)
    tx = pd.concat([tx, dup]).sort_values(["Date", "Transaction ID"], kind="stable").reset_index(drop=True)
    k3["exact_duplicate_rows"] = 60
    k3["rows_including_duplicates"] = len(tx)
    _write_xlsx(tx, t["products"], raw / "kb_raw_transactions.xlsx")
    key["ch03_kb_raw_transactions"] = k3

    # ------------------------------------------------------------------ Ch 6
    mo = o.sample(8000, random_state=seed).merge(cust[["customer_id", "phone"]], on="customer_id")
    df = pd.DataFrame({
        "order_id": mo.order_id, "order_date": mo.order_dt, "customer_id": mo.customer_id,
        "customer_phone": mo.phone, "province": mo.province, "channel": mo.channel,
        "delivery_method": mo.delivery_method, "items": mo["items"].astype(object),
        "subtotal_zmw": mo.subtotal_zmw, "discount_zmw": mo.discount_zmw,
        "delivery_fee_zmw": mo.delivery_fee_zmw.astype(object), "total": mo.total_zmw.astype(object),
        "payment_method": mo.method, "status": mo.status})
    n = len(df)
    k6 = {"clean_rows": n}
    fmt = rng.choice(["iso", "dmy", "text"], n, p=[0.60, 0.25, 0.15])
    df["order_date"] = [d.strftime("%Y-%m-%d %H:%M:%S") if f == "iso" else
                        d.strftime("%d/%m/%Y") if f == "dmy" else d.strftime("%d %b %Y")
                        for d, f in zip(df.order_date, fmt)]
    k6["date_formats"] = {"YYYY-MM-DD HH:MM:SS": int((fmt == "iso").sum()),
                          "DD/MM/YYYY": int((fmt == "dmy").sum()), "DD Mon YYYY": int((fmt == "text").sum())}
    variants = {"Copperbelt": ["Copper Belt", "CB", "copperbelt", "COPPERBELT"],
                "Lusaka": ["LUSAKA", "Lsk", " Lusaka", "lusaka"],
                "North-Western": ["North Western", "NW", "Northwestern", "north-western"],
                "Southern": ["southern", "Southern "], "Central": ["central", "CENTRAL"],
                "Eastern": ["eastern", "Eastern "], "Northern": ["northern"], "Muchinga": ["muchinga"],
                "Luapula": ["luapula", "Luapula "], "Western": ["western", "WESTERN"]}
    m = rng.random(n) < 0.11
    df.loc[m, "province"] = [rng.choice(variants[p]) for p in df.province[m]]
    k6["province_variant_rows"] = int(m.sum())
    m = rng.random(n) < 0.20
    df.loc[m, "total"] = [_kwacha(v) for v in mo.total_zmw[m]]
    k6["total_as_text_rows"] = int(m.sum())
    phone_fmt = rng.choice(["intl", "local", "spaced", "nozero"], n, p=[0.55, 0.25, 0.12, 0.08])
    def ph(p, f):
        d = p[4:]
        return {"intl": p, "local": "0" + d, "spaced": f"0{d[:2]} {d[2:5]} {d[5:]}", "nozero": "260" + d}[f]
    df["customer_phone"] = [ph(p, f) for p, f in zip(df.customer_phone, phone_fmt)]
    k6["phone_formats"] = {k: int((phone_fmt == k).sum()) for k in ["intl", "local", "spaced", "nozero"]}
    miss = {}
    for col, rate in [("channel", 0.03), ("delivery_fee_zmw", 0.02), ("province", 0.01), ("customer_phone", 0.02)]:
        m = rng.random(n) < rate
        df.loc[m, col] = np.nan
        miss[col] = int(m.sum())
    k6["missing_values_planted"] = miss
    neg = rng.choice(n, 25, replace=False)
    df.loc[neg, "items"] = -df.loc[neg, "items"].astype(int)
    k6["negative_items_rows"] = sorted(df.order_id.iloc[neg].tolist())
    shift = rng.choice(np.setdiff1d(np.arange(n), neg), 5, replace=False)
    for i in shift:
        df.loc[i, "subtotal_zmw"] = round(float(df.loc[i, "subtotal_zmw"]) * 100, 2)
    k6["decimal_shift_subtotal_x100_orders"] = sorted(df.order_id.iloc[shift].tolist())
    exact = df.sample(150, random_state=seed + 6)
    near = df.drop(exact.index).sample(40, random_state=seed + 7).copy()
    near["channel"] = near.channel.str.upper()
    near["customer_id"] = near.customer_id + " "
    df = pd.concat([df, exact, near]).sample(frac=1, random_state=seed).reset_index(drop=True)
    k6["exact_duplicates"] = 150
    k6["near_duplicates_channel_upper_and_trailing_space_in_customer_id"] = 40
    k6["rows_in_file"] = len(df)
    df.to_csv(raw / "kb_orders_messy.csv", index=False)
    key["ch06_kb_orders_messy"] = k6

    # ------------------------------------------------------------------ Ch 7
    top_cat = items.merge(ok[["order_id", "customer_id"]], on="order_id") \
        .groupby(["customer_id", "category"]).line_total_zmw.sum().reset_index() \
        .sort_values("line_total_zmw", kind="stable").groupby("customer_id").category.last()
    ret_n = t["returns"].merge(o[["order_id", "customer_id"]], on="order_id").groupby("customer_id").size()
    g = ok.groupby("customer_id").agg(orders=("order_id", "count"), total_spend_zmw=("total_zmw", "sum"),
                                      first_order=("order_dt", "min"), last_order=("order_dt", "max"))
    d7 = cust.join(g, on="customer_id", how="inner")
    d7["age_band"] = pd.cut(d7.age, AGE_BINS, labels=AGE_LABELS)
    d7["tenure_days"] = (pd.Timestamp("2025-12-31") - pd.to_datetime(d7.signup_date)).dt.days
    d7["avg_basket_zmw"] = (d7.total_spend_zmw / d7.orders).round(2)
    d7["total_spend_zmw"] = d7.total_spend_zmw.round(2)
    d7["recency_days"] = (pd.Timestamp("2025-12-31") - d7.last_order.dt.normalize()).dt.days
    d7["first_order_date"] = d7.first_order.dt.date
    d7["last_order_date"] = d7.last_order.dt.date
    d7["preferred_payment"] = d7.customer_id.map(pref_pay)
    d7["top_category"] = d7.customer_id.map(top_cat)
    d7["returns_count"] = d7.customer_id.map(ret_n).fillna(0).astype(int)
    d7["avg_rating_given"] = d7.customer_id.map(avg_rating).round(2)
    d7[["customer_id", "gender", "age", "age_band", "province", "town", "signup_channel", "loyalty_tier",
        "tenure_days", "orders", "total_spend_zmw", "avg_basket_zmw", "first_order_date", "last_order_date",
        "recency_days", "preferred_payment", "top_category", "returns_count", "avg_rating_given"]] \
        .to_csv(clean / "kb_customer_demographics.csv", index=False)

    # ------------------------------------------------------------------ Ch 8
    li = items.merge(ok[["order_id", "order_dt", "province"]], on="order_id")
    li["month"] = li.order_dt.dt.to_period("M").astype(str)
    rr = t["returns"].merge(o[["order_id", "province", "order_dt"]], on="order_id") \
        .merge(t["products"][["product_id", "category"]], on="product_id")
    rr["month"] = rr.order_dt.dt.to_period("M").astype(str)
    kpi = li.groupby(["month", "category", "province"]).agg(
        orders=("order_id", "nunique"), units=("quantity", "sum"),
        revenue_zmw=("line_total_zmw", "sum"), cost_zmw=("line_cost_zmw", "sum")).reset_index()
    kpi["gross_margin_zmw"] = (kpi.revenue_zmw - kpi.cost_zmw).round(2)
    kpi["revenue_zmw"] = kpi.revenue_zmw.round(2)
    kpi = kpi.drop(columns="cost_zmw").merge(
        rr.groupby(["month", "category", "province"]).size().rename("returns").reset_index(),
        how="left", on=["month", "category", "province"])
    kpi["returns"] = kpi.returns.fillna(0).astype(int)
    kpi.to_csv(clean / "kb_monthly_kpis.csv", index=False)

    # ------------------------------------------------------------------ Ch 10
    dv = t["deliveries"].dropna(subset=["delivered_at"]).merge(o[["order_id", "order_dt", "province"]], on="order_id")
    dv["delivery_hours"] = ((pd.to_datetime(dv.delivered_at) - dv.order_dt).dt.total_seconds() / 3600).round(2)
    dv["sla_hours"] = dv.province.map(SLA)
    dv["order_month"] = dv.order_dt.dt.month
    dv.rename(columns={"order_dt": "order_datetime"})[[
        "order_id", "province", "courier", "distance_km", "order_datetime", "delivered_at",
        "delivery_hours", "sla_hours", "delayed_flag", "order_month"]].to_csv(clean / "kb_delivery_times.csv", index=False)

    n_ab = 5000
    grp = np.repeat(["WhatsApp", "SMS"], n_ab)
    conv_p = np.where(grp == "WhatsApp", 0.061, 0.050)
    clicked = rng.random(2 * n_ab) < np.where(grp == "WhatsApp", 0.21, 0.12)
    converted = rng.random(2 * n_ab) < conv_p
    clicked = clicked | converted
    value = np.where(converted, np.round(rng.gamma(4.0, 160, 2 * n_ab) + 80, 2), np.nan)
    ab = pd.DataFrame({
        "contact_id": [f"AB{i:05d}" for i in range(1, 2 * n_ab + 1)], "group": grp,
        "province": rng.choice(list(SLA), 2 * n_ab, p=[.32, .22, .10, .08, .07, .05, .03, .04, .05, .04]),
        "age_band": rng.choice(AGE_LABELS, 2 * n_ab, p=[.22, .36, .23, .12, .07]),
        "existing_customer": (rng.random(2 * n_ab) < 0.55).astype(int),
        "sent_date": "2025-08-04", "clicked": clicked.astype(int), "converted": converted.astype(int),
        "order_value_zmw": value}).sample(frac=1, random_state=seed).reset_index(drop=True)
    ab.to_csv(clean / "kb_campaign_ab.csv", index=False)
    from scipy import stats
    tab = ab.groupby("group").converted.agg(["sum", "count"])
    p1, p2 = tab.loc["WhatsApp", "sum"] / tab.loc["WhatsApp", "count"], tab.loc["SMS", "sum"] / tab.loc["SMS", "count"]
    chi = stats.chi2_contingency([[tab.loc["WhatsApp", "sum"], tab.loc["WhatsApp", "count"] - tab.loc["WhatsApp", "sum"]],
                                  [tab.loc["SMS", "sum"], tab.loc["SMS", "count"] - tab.loc["SMS", "sum"]]], correction=False)
    key["ch10_campaign_ab"] = {"conversion_whatsapp": round(float(p1), 4), "conversion_sms": round(float(p2), 4),
                               "chi2_p_value": round(float(chi.pvalue), 4)}
    pay = t["payments"].merge(hidden["is_fraud"], on="payment_id")
    flagged = pay[pay.fraud_flag == 1]
    key["ch10_fraud_flag"] = {"base_rate": round(float(pay.is_fraud.mean()), 4),
                              "sensitivity": round(float(pay[pay.is_fraud == 1].fraud_flag.mean()), 3),
                              "false_positive_rate": round(float(pay[pay.is_fraud == 0].fraud_flag.mean()), 4),
                              "P_fraud_given_flag": round(float(flagged.is_fraud.mean()), 3)}

    # ------------------------------------------------------------------ Ch 11 / 13
    pr = t["products"].merge(t["suppliers"][["supplier_id", "country"]], on="supplier_id") \
        .rename(columns={"country": "supplier_country"})
    pr[["product_id", "product_name", "category", "subcategory", "brand", "brand_tier", "supplier_country",
        "imported_flag", "weight_kg", "unit_cost_zmw", "list_price_zmw"]].to_csv(clean / "kb_product_pricing.csv", index=False)

    # ------------------------------------------------------------------ Ch 12
    before = ok[ok.order_dt <= SNAPSHOT]
    win180 = before[before.order_dt > SNAPSHOT - pd.Timedelta(days=180)]
    elig = win180.customer_id.unique()
    after = ok[(ok.order_dt > SNAPSHOT) & (ok.order_dt <= SNAPSHOT + pd.Timedelta(days=90))]
    b = before[before.customer_id.isin(elig)]
    dl = t["deliveries"][["order_id", "delayed_flag"]]
    b = b.merge(dl, on="order_id", how="left")
    gb = b.groupby("customer_id")
    f = pd.DataFrame({
        "orders_total": gb.order_id.count(),
        "orders_last_90d": b[b.order_dt > SNAPSHOT - pd.Timedelta(days=90)].groupby("customer_id").size(),
        "orders_last_180d": win180.groupby("customer_id").size(),
        "spend_last_180d_zmw": win180.groupby("customer_id").total_zmw.sum().round(2),
        "avg_basket_zmw": gb.total_zmw.mean().round(2),
        "recency_days": (SNAPSHOT - gb.order_dt.max()).dt.days,
        "days_since_first_order": (SNAPSHOT - gb.order_dt.min()).dt.days,
        "pct_orders_delayed": gb.delayed_flag.mean().fillna(0).round(3),
        "pct_orders_campaign": gb.campaign_id.apply(lambda s: s.notna().mean()).round(3),
        "app_share": gb.channel.apply(lambda s: (s == "App").mean()).round(3),
    }).loc[elig]
    f["orders_last_90d"] = f.orders_last_90d.fillna(0).astype(int)
    rb = t["returns"].merge(o[["order_id", "customer_id"]], on="order_id")
    rb = rb[pd.to_datetime(rb.returned_at) <= SNAPSHOT]
    f["returns_count"] = rb.groupby("customer_id").size().reindex(f.index).fillna(0).astype(int)
    rv = rev[pd.to_datetime(rev.review_date) <= SNAPSHOT]
    f["avg_rating_given"] = rv.groupby("customer_id").rating.mean().reindex(f.index).round(2)
    f["preferred_payment"] = b.groupby("customer_id").method.agg(lambda s: s.mode().iat[0])
    f = f.join(cust.set_index("customer_id")[["gender", "age", "province", "signup_channel", "signup_date"]])
    f["tenure_days"] = (SNAPSHOT.normalize() - pd.to_datetime(f.signup_date)).dt.days
    f["churned"] = (~f.index.isin(after.customer_id)).astype(int)
    f = f.drop(columns="signup_date").reset_index().rename(columns={"index": "customer_id"})
    lead = ["customer_id", "gender", "age", "province", "signup_channel", "tenure_days"]
    f = f[lead + [c for c in f.columns if c not in lead]]
    f.to_csv(clean / "kb_customer_churn.csv", index=False)
    key["ch12_churn"] = {"rows": len(f), "churn_rate": round(float(f.churned.mean()), 3),
                         "snapshot": "2025-09-30", "outcome_window_days": 90}

    # ------------------------------------------------------------------ Ch 14
    rs = t["reviews"].merge(t["products"][["product_id", "category"]], on="product_id") \
        .merge(o[["order_id", "province"]], on="order_id").sample(1000, random_state=seed)
    rs.sort_values("review_date", kind="stable")[["review_id", "review_date", "province", "category", "rating", "review_text"]] \
        .to_csv(clean / "kb_reviews_sample.csv", index=False)

    # ------------------------------------------------------------------ unseen
    key["unseen"] = _make_unseen(rng, unseen)
    return key


def _write_xlsx(tx, products, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws.append(list(tx.columns))
    for row in tx.itertuples(index=False):
        ws.append([v.to_pydatetime() if isinstance(v, pd.Timestamp) else v for v in row])
    for cell in ws["B"][1:]:
        cell.number_format = "DD/MM/YYYY"
    for cell in ws["I"][1:]:
        if isinstance(cell.value, float):
            cell.number_format = '"K"#,##0.00'
    hdr = Font(bold=True, color="FFFFFF")
    for c in ws[1]:
        c.font, c.fill = hdr, PatternFill("solid", fgColor="1B2A41")
    for col, w in zip("ABCDEFGHIJ", [16, 12, 24, 15, 11, 44, 17, 6, 12, 18]):
        ws.column_dimensions[col].width = w
    ws2 = wb.create_sheet("Products")
    ws2.append(["Product ID", "Product Name", "Category", "Unit Cost (ZMW)"])
    for r in products[["product_id", "product_name", "category", "unit_cost_zmw"]].itertuples(index=False):
        ws2.append(list(r))
    for c in ws2[1]:
        c.font, c.fill = hdr, PatternFill("solid", fgColor="1B2A41")
    for cell in ws2["D"][1:]:
        cell.number_format = '"K"#,##0.00'
    for col, w in zip("ABCD", [12, 44, 18, 16]):
        ws2.column_dimensions[col].width = w
    wb.save(path)


def _make_unseen(rng, folder: Path) -> dict:
    # 1. FinTech loans — comma-separated, UTF-8, some missing values
    n = 1200
    income = np.round(rng.lognormal(8.6, 0.55, n), -1)
    amount = np.round(income * rng.uniform(0.3, 3.0, n), -1)
    mm = rng.poisson(45, n)
    logit = -2.2 + 0.9 * (amount / income) - 0.015 * mm
    loans = pd.DataFrame({
        "loan_id": [f"LN{i:05d}" for i in range(1, n + 1)],
        "application_date": (pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 700, n), "D")).date,
        "applicant_age": rng.integers(19, 66, n), "monthly_income_zmw": income,
        "loan_amount_zmw": amount, "term_months": rng.choice([3, 6, 12, 24], n),
        "purpose": rng.choice(["School fees", "Business stock", "Medical", "Farming inputs", "Rent", "Other"], n),
        "mobile_money_tx_90d": mm, "defaulted": (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)})
    loans.loc[rng.random(n) < 0.04, "monthly_income_zmw"] = np.nan
    loans.loc[rng.random(n) < 0.02, "purpose"] = np.nan
    loans.to_csv(folder / "fintech_loans.csv", index=False)
    # 2. Clinic visits — semicolon-delimited
    n = 900
    clinic = pd.DataFrame({
        "visit_id": [f"V{i:05d}" for i in range(1, n + 1)],
        "visit_date": (pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 330, n), "D")).strftime("%d/%m/%Y"),
        "clinic": rng.choice(["Kabwata", "Chelstone", "Matero", "Kalingalinga"], n),
        "patient_age": rng.integers(0, 90, n), "sex": rng.choice(["F", "M"], n, p=[.56, .44]),
        "visit_reason": rng.choice(["Malaria test", "Antenatal", "Child immunisation", "Hypertension review",
                                    "General consultation", "Dental"], n),
        "wait_minutes": np.round(rng.gamma(3, 18, n)).astype(int),
        "consultation_fee_zmw": rng.choice([0, 50, 100, 150], n, p=[.35, .3, .25, .1]),
        "follow_up": rng.choice(["Yes", "No"], n, p=[.3, .7])})
    clinic.to_csv(folder / "clinic_visits.csv", index=False, sep=";")
    # 3. Marketing leads — Latin-1 encoded (accented campaign names)
    n = 700
    leads = pd.DataFrame({
        "lead_id": [f"LD{i:04d}" for i in range(1, n + 1)],
        "source": rng.choice(["Facebook", "LinkedIn", "Referral", "Website", "Trade show"], n),
        "campaign": rng.choice(["Café Owners Q2", "Agri Expo 2025", "Résumé Clinic", "SME Growth Week"], n),
        "sector": rng.choice(["Hospitality", "Agriculture", "Retail", "Education", "Mining services"], n),
        "lead_score": rng.integers(1, 101, n), "contacted": rng.choice(["Y", "N"], n, p=[.7, .3])})
    conv = (leads.contacted == "Y") & (rng.random(n) < leads.lead_score / 220)
    leads["converted"] = conv.astype(int)
    leads["deal_value_zmw"] = np.where(conv, np.round(rng.gamma(2, 9000, n), -2), np.nan)
    leads.to_csv(folder / "marketing_leads.csv", index=False, encoding="latin-1")
    return {"fintech_loans.csv": "comma, UTF-8, missing income/purpose",
            "clinic_visits.csv": "semicolon delimiter, DD/MM/YYYY dates",
            "marketing_leads.csv": "Latin-1 encoding (accented campaign names)"}
