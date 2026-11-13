"""
Kwacha Basket Ltd — synthetic dataset generator
================================================
Companion data for *Data Analysis for Beginners: From Excel to AI-Powered
Analytics and Machine Learning* (DevDash Innovations).

Kwacha Basket Ltd and every person in this data are FICTIONAL. Names are
random combinations of common Zambian first names and surnames.

Usage (from the repository root):
    python data/generator/generate_data.py            # writes into data/
    python data/generator/generate_data.py --out DIR  # writes elsewhere

Everything is driven by one seed (2026), so every reader gets identical
files. Do not change SEED: the book's printed results depend on it.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026
START = pd.Timestamp("2023-01-01")
END = pd.Timestamp("2025-12-31")
SNAPSHOT = pd.Timestamp("2025-09-30")  # churn snapshot (Chapter 12)

rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------
PROVINCES = {
    # province: (share of customers, towns, remoteness 0-1, delivery SLA hours)
    "Lusaka": (0.32, ["Lusaka", "Chongwe", "Kafue"], 0.00, 24),
    "Copperbelt": (0.22, ["Kitwe", "Ndola", "Chingola", "Mufulira", "Luanshya"], 0.20, 48),
    "Southern": (0.10, ["Livingstone", "Choma", "Mazabuka", "Monze"], 0.35, 72),
    "Central": (0.08, ["Kabwe", "Kapiri Mposhi", "Mkushi"], 0.25, 48),
    "Eastern": (0.07, ["Chipata", "Petauke", "Katete"], 0.55, 96),
    "Northern": (0.05, ["Kasama", "Mbala", "Mporokoso"], 0.80, 120),
    "Muchinga": (0.03, ["Chinsali", "Mpika", "Nakonde"], 0.75, 120),
    "Luapula": (0.04, ["Mansa", "Samfya", "Kawambwa"], 0.75, 120),
    "North-Western": (0.05, ["Solwezi", "Kasempa", "Mwinilunga"], 0.65, 96),
    "Western": (0.04, ["Mongu", "Senanga", "Kaoma"], 0.85, 120),
}
PICKUP_PROVINCES = {"Lusaka", "Copperbelt", "Southern"}  # Lusaka, Kitwe, Ndola, Livingstone
BASE_DISTANCE = {  # km from the nearest Kwacha Basket hub
    "Lusaka": (3, 30), "Copperbelt": (3, 60), "Southern": (5, 380), "Central": (40, 260),
    "Eastern": (300, 600), "Northern": (700, 900), "Muchinga": (550, 1000),
    "Luapula": (250, 450), "North-Western": (180, 450), "Western": (500, 700),
}

FEMALE = ["Mwila", "Chanda", "Mutale", "Bwalya", "Chilufya", "Natasha", "Grace", "Mercy",
          "Thandiwe", "Mapalo", "Taonga", "Luyando", "Mutinta", "Namakau", "Inonge",
          "Chileshe", "Tiyamike", "Precious", "Prudence", "Memory", "Charity", "Mirriam",
          "Esther", "Ruth", "Agnes", "Beatrice", "Loveness", "Febby", "Towela", "Maureen",
          "Chipo", "Nchimunya", "Kasuba", "Lweendo", "Mwangala", "Patricia", "Joyce", "Faith"]
MALE = ["Mulenga", "Musonda", "Joseph", "John", "Brian", "Kelvin", "Mwape", "Kalaba",
        "Lombe", "Mubanga", "Kondwani", "Gift", "Emmanuel", "Moses", "Patrick", "Victor",
        "Davies", "Lazarus", "Chisomo", "Mwansa", "Kabwe", "Chikondi", "Peter", "Elijah",
        "Isaac", "Mutinta", "Hamweemba", "Sipho", "Chola", "Kapambwe", "Mwenya", "Daniel",
        "Stephen", "Martin", "Allan", "Bupe", "Kangwa", "Felix"]
SURNAMES = ["Banda", "Phiri", "Mwale", "Tembo", "Zulu", "Daka", "Lungu", "Mulenga", "Chanda",
            "Bwalya", "Musonda", "Mutale", "Kabwe", "Mwansa", "Sakala", "Ngoma", "Mumba",
            "Kunda", "Siame", "Simukonda", "Hamoonga", "Hachinga", "Mweemba", "Moonga",
            "Chileshe", "Kapembwa", "Lubinda", "Mubita", "Nyirenda", "Sichone", "Chisenga",
            "Kasonde", "Mbewe", "Nkhoma", "Chibwe", "Kangwa", "Mwila", "Ng'andu", "Shawa",
            "Siwale", "Kalunga", "Mbao", "Chama", "Haamoonga", "Simwanza", "Kaunda"]

# category: share of item lines, subcategories {name: (cost range ZMW, weight range kg)}
CATALOGUE = {
    "Groceries": (0.30, 0.25, {
        "Mealie Meal": ((90, 260), (10, 25)), "Cooking Oil": ((45, 160), (1, 5)),
        "Rice": ((35, 140), (1, 10)), "Sugar": ((30, 120), (1, 10)),
        "Kapenta & Fish": ((40, 180), (0.5, 2)), "Beverages": ((12, 90), (0.5, 3)),
        "Canned Foods": ((15, 60), (0.4, 1)), "Snacks": ((8, 45), (0.1, 0.5))}),
    "Household": (0.14, 0.32, {
        "Laundry": ((25, 120), (0.5, 5)), "Cleaning": ((18, 90), (0.5, 2)),
        "Toiletries": ((10, 70), (0.2, 1)), "Candles & Lighting": ((15, 160), (0.2, 2))}),
    "Electronics": (0.08, 0.30, {
        "Mobile Phones": ((900, 7500), (0.15, 0.4)), "Phone Accessories": ((40, 450), (0.05, 0.3)),
        "Solar & Power": ((350, 4800), (1, 12)), "Audio": ((180, 2500), (0.2, 3)),
        "Small Appliances": ((300, 2800), (1, 6))}),
    "Fashion": (0.09, 0.55, {
        "Chitenge Fabric": ((60, 260), (0.4, 1)), "Footwear": ((150, 900), (0.6, 1.5)),
        "Menswear": ((120, 750), (0.3, 1)), "Womenswear": ((120, 850), (0.3, 1)),
        "School Uniforms": ((90, 380), (0.3, 1))}),
    "Health & Beauty": (0.12, 0.45, {
        "Skin Care": ((25, 320), (0.1, 0.6)), "Hair Care": ((20, 260), (0.1, 0.8)),
        "First Aid": ((15, 180), (0.1, 0.8)), "Fragrance": ((90, 900), (0.1, 0.4))}),
    "Baby & Kids": (0.08, 0.40, {
        "Nappies": ((70, 320), (1, 4)), "Baby Food": ((30, 140), (0.3, 1)),
        "Toys": ((40, 600), (0.2, 2))}),
    "Home & Kitchen": (0.10, 0.38, {
        "Cookware": ((90, 1200), (0.8, 5)), "Bedding": ((150, 1100), (1, 4)),
        "Storage": ((30, 300), (0.3, 3)), "Tableware": ((40, 450), (0.4, 3))}),
    "Stationery": (0.09, 0.35, {
        "Exercise Books": ((10, 80), (0.2, 1.5)), "Pens & Pencils": ((5, 60), (0.05, 0.3)),
        "School Bags": ((90, 450), (0.4, 1.2)), "Calculators": ((60, 480), (0.1, 0.4))}),
}
BRAND_STEMS = ["Zambezi", "Kafue", "Luangwa", "Mukuba", "Chisamba", "Kariba", "Lunsemfwa",
               "Mosi", "Nsefu", "Bangweulu", "Mulungushi", "Kalambo", "Ngoma", "Tonga",
               "Lozi", "Savanna", "Copperline", "Sunrise", "Baobab", "Msasa", "Mopane",
               "Kwacha", "Chilenje", "Kabulonga", "Mutanda", "Tanganyika", "Mweru", "Kasanka"]
BRAND_SUFFIX = {"Value": ["Basics", "Everyday", "Choice"], "Standard": ["Home", "Plus", "Co."],
                "Premium": ["Select", "Gold", "Prestige"]}
SUPPLIER_COUNTRIES = (["Zambia"] * 20 + ["South Africa"] * 7 + ["China"] * 5 + ["Tanzania"] * 3
                      + ["Kenya"] * 2 + ["United Arab Emirates"] * 2 + ["India"] * 1)

PAY_METHODS = ["Airtel Money", "MTN MoMo", "Zamtel Kwacha", "Card", "Cash on Delivery"]
PAY_P = [0.30, 0.26, 0.06, 0.18, 0.20]
COURIERS = ["Zed Express", "Copperline Couriers", "Kwacha Basket Fleet"]
CAMPAIGN_CHANNELS = ["Facebook", "WhatsApp", "SMS", "Google", "Radio"]
VAT = 0.16


def money(x):
    return np.round(np.asarray(x, dtype=float), 2)


# ---------------------------------------------------------------------------
# 1. Suppliers and products
# ---------------------------------------------------------------------------
def make_suppliers() -> pd.DataFrame:
    stems = rng.choice(BRAND_STEMS, size=40, replace=True)
    kinds = rng.choice(["Distributors", "Trading", "Wholesale", "Imports", "Supplies", "Ltd"], 40)
    countries = np.array(SUPPLIER_COUNTRIES)
    rng.shuffle(countries)
    lead = np.where(countries == "Zambia", rng.integers(2, 10, 40), rng.integers(14, 60, 40))
    names = [f"{s} {k}" for s, k in zip(stems, kinds)]
    # make names unique
    seen = {}
    for i, n in enumerate(names):
        seen[n] = seen.get(n, 0) + 1
        if seen[n] > 1:
            names[i] = f"{n} {seen[n]}"
    return pd.DataFrame({"supplier_id": [f"S{i:03d}" for i in range(1, 41)],
                         "supplier_name": names, "country": countries,
                         "lead_time_days": lead})


def make_products(suppliers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    n_total = 600
    shares = np.array([v[0] for v in CATALOGUE.values()])
    counts = np.round(shares / shares.sum() * n_total).astype(int)
    counts[0] += n_total - counts.sum()
    cat_effect = {"Groceries": 0.00, "Household": 0.04, "Electronics": 0.10, "Fashion": 0.30,
                  "Health & Beauty": 0.22, "Baby & Kids": 0.12, "Home & Kitchen": 0.18,
                  "Stationery": 0.15}
    tier_effect = {"Value": 0.00, "Standard": 0.08, "Premium": 0.22}
    pid = 1
    for (cat, (_, ret_rate, subs)), n in zip(CATALOGUE.items(), counts):
        sub_names = list(subs)
        for _ in range(n):
            sub = sub_names[rng.integers(len(sub_names))]
            (c_lo, c_hi), (w_lo, w_hi) = subs[sub]
            tier = rng.choice(["Value", "Standard", "Premium"], p=[0.40, 0.40, 0.20])
            weight = rng.uniform(w_lo, w_hi)
            pos = rng.beta(2, 3)  # position within cost range
            pos = min(1.0, pos + {"Value": -0.10, "Standard": 0.0, "Premium": 0.20}[tier])
            pos = max(0.0, pos)
            cost = c_lo + pos * (c_hi - c_lo)
            sup = suppliers.sample(1, random_state=int(rng.integers(1e9))).iloc[0]
            imported = int(sup["country"] != "Zambia")
            if cat == "Electronics" and rng.random() < 0.7 and not imported:
                sup = suppliers[suppliers.country != "Zambia"].sample(
                    1, random_state=int(rng.integers(1e9))).iloc[0]
                imported = 1
            markup = 1.28 + cat_effect[cat] + tier_effect[tier] + 0.06 * imported
            price = cost * (markup + rng.normal(0, 0.24)) + 4.0 * weight + rng.normal(0, 6)
            price = max(price, cost * 1.05)
            # psychological price endings
            price = np.floor(price) + rng.choice([0.0, 0.50, 0.99], p=[0.5, 0.2, 0.3])
            brand = f"{rng.choice(BRAND_STEMS)} {rng.choice(BRAND_SUFFIX[tier])}"
            size = f"{weight:.1f}kg" if weight >= 1 else f"{int(round(weight * 1000, -1))}g"
            rows.append({
                "product_id": f"P{pid:04d}", "sku": f"KB-{cat[:3].upper()}-{pid:05d}",
                "product_name": f"{brand} {sub} {size}", "category": cat,
                "subcategory": sub, "brand": brand, "brand_tier": tier,
                "supplier_id": sup["supplier_id"], "unit_cost_zmw": round(cost, 2),
                "list_price_zmw": round(price, 2), "weight_kg": round(weight, 2),
                "imported_flag": imported,
                "launch_date": (pd.Timestamp("2021-01-01") + pd.Timedelta(
                    days=int(rng.integers(0, 1700)))).date().isoformat(),
            })
            pid += 1
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Calendar weights (trend, seasonality, payday, campaigns)
# ---------------------------------------------------------------------------
def make_campaigns() -> pd.DataFrame:
    rows = []
    for i, month in enumerate(pd.date_range(START, END, freq="MS")):
        ch = CAMPAIGN_CHANNELS[i % 5]
        start = month + pd.Timedelta(days=int(rng.integers(3, 12)))
        length = int(rng.integers(7, 15))
        theme = {12: "Festive Season", 1: "Back to School", 5: "Term Two Ready",
                 9: "Term Three Ready", 3: "Women's Month", 10: "Independence Deals",
                 11: "Black Friday", 6: "Mid-Year Sale"}.get(month.month, "Monthly Savers")
        rows.append({"campaign_id": f"C{i + 1:03d}",
                     "campaign_name": f"{theme} {month.year} ({ch})", "channel": ch,
                     "start_date": start.date().isoformat(),
                     "end_date": (start + pd.Timedelta(days=length)).date().isoformat(),
                     "budget_zmw": float(round(rng.uniform(5000, 45000), -2))})
    return pd.DataFrame(rows)


def day_weights(campaigns: pd.DataFrame) -> pd.Series:
    days = pd.date_range(START, END, freq="D")
    t = (days - START).days / 365.25
    w = np.exp(0.10 * np.asarray(t, dtype=float))  # underlying demand growth
    month_f = {1: 0.88, 2: 0.92, 3: 0.97, 4: 0.97, 5: 1.0, 6: 0.98, 7: 0.97, 8: 1.0,
               9: 1.02, 10: 1.05, 11: 1.15, 12: 1.42}
    w = w * np.array([month_f[m] for m in days.month])
    payday = (days.day >= 25) | (days.day <= 2)
    w *= np.where(payday, 1.35, 1.0)
    dow_f = np.array([0.95, 0.95, 0.97, 1.0, 1.12, 1.12, 0.89])  # Mon..Sun
    w *= dow_f[days.day_of_week]
    for _, c in campaigns.iterrows():
        mask = np.asarray((days >= c.start_date) & (days <= c.end_date))
        w[mask] *= 1.08  # real but modest uplift
    return pd.Series(w, index=days)


# ---------------------------------------------------------------------------
# 3. Customers
# ---------------------------------------------------------------------------
def make_customers(n=5000) -> pd.DataFrame:
    prov_names = list(PROVINCES)
    prov = rng.choice(prov_names, size=n, p=[PROVINCES[p][0] for p in prov_names])
    towns = [PROVINCES[p][1][min(int(rng.exponential(0.9)), len(PROVINCES[p][1]) - 1)] for p in prov]
    gender = rng.choice(["F", "M"], size=n, p=[0.53, 0.47])
    first = np.where(gender == "F", rng.choice(FEMALE, n), rng.choice(MALE, n))
    last = rng.choice(SURNAMES, n)
    birth_year = np.clip(np.round(2025 - (18 + rng.gamma(4.0, 4.6, n))), 1955, 2007).astype(int)
    # signups accelerate over time; ~12% joined before 2023
    span = (END - pd.Timestamp("2021-09-01")).days
    u = rng.beta(1.10, 1.0, n)
    signup = pd.Timestamp("2021-09-01") + pd.to_timedelta((u * (span - 20)).astype(int), "D")
    channel = rng.choice(["Web", "App", "WhatsApp"], n, p=[0.42, 0.33, 0.25])
    prefix = rng.choice(["95", "96", "76", "97", "77"], n, p=[0.08, 0.30, 0.10, 0.35, 0.17])
    phone = [f"+260{p}{rng.integers(1000000, 9999999)}" for p in prefix]
    return pd.DataFrame({
        "customer_id": [f"CU{i:05d}" for i in range(1, n + 1)],
        "first_name": first, "last_name": last, "gender": gender,
        "birth_year": birth_year, "province": prov, "town": towns, "phone": phone,
        "signup_date": signup.normalize(), "signup_channel": channel,
    })


# ---------------------------------------------------------------------------
# 4. Orders (per-customer activity windows, seasonal day sampling)
# ---------------------------------------------------------------------------
def make_orders(customers: pd.DataFrame, weights: pd.Series, campaigns: pd.DataFrame):
    n = len(customers)
    remote = customers.province.map(lambda p: PROVINCES[p][2]).to_numpy()
    age = 2025 - customers.birth_year.to_numpy()
    app = (customers.signup_channel == "App").to_numpy()
    # latent loyalty drives both purchase rate and lifetime
    loyalty = rng.normal(0, 1, n)
    rate = np.exp(-3.82 + 0.55 * loyalty + 0.25 * app - 0.25 * remote)  # orders per day
    life_mean = np.exp(7.0 + 0.45 * loyalty + 0.25 * app - 0.70 * remote + 0.004 * (age - 35))
    lifetime = rng.exponential(life_mean)
    start = customers.signup_date.to_numpy()
    end = start + pd.to_timedelta(lifetime.astype(int), "D").to_numpy()

    days = weights.index
    cw = np.concatenate([[0.0], np.cumsum(weights.to_numpy())])
    day_idx = lambda ts: np.clip(((pd.DatetimeIndex(ts) - START).days).to_numpy(), 0, len(days))
    a = day_idx(np.maximum(start, np.datetime64(START)))
    b = day_idx(np.minimum(end, np.datetime64(END + pd.Timedelta(days=1))))
    active = np.maximum(b - a, 0)
    mean_w = weights.mean()
    expected = rate * (cw[b] - cw[a]) / mean_w
    counts = rng.poisson(expected)
    counts[(active == 0)] = 0

    cust_idx = np.repeat(np.arange(n), counts)
    lo, hi = cw[a][cust_idx], cw[b][cust_idx]
    target = lo + rng.random(len(cust_idx)) * (hi - lo)
    d = np.searchsorted(cw, target, side="right") - 1
    d = np.clip(d, 0, len(days) - 1)
    hours = rng.choice(np.arange(24), len(d), p=_hour_profile())
    mins = rng.integers(0, 60, len(d))
    secs = rng.integers(0, 60, len(d))
    ts = (days[d] + pd.to_timedelta(hours, "h") + pd.to_timedelta(mins, "m")
          + pd.to_timedelta(secs, "s"))
    orders = pd.DataFrame({"customer_idx": cust_idx, "order_datetime": ts})
    orders = orders.sort_values("order_datetime", kind="stable").reset_index(drop=True)
    latent = pd.DataFrame({"loyalty": loyalty, "remote": remote, "lifetime_days": lifetime})
    return orders, latent


def _hour_profile():
    h = np.arange(24)
    p = 0.15 + np.exp(-((h - 13) ** 2) / 6) + 1.2 * np.exp(-((h - 20) ** 2) / 5) \
        + 0.5 * np.exp(-((h - 8) ** 2) / 3)
    p[(h >= 1) & (h <= 5)] *= 0.15
    return p / p.sum()


# ---------------------------------------------------------------------------
# 5. Main build
# ---------------------------------------------------------------------------
def build():
    suppliers = make_suppliers()
    products = make_products(suppliers)
    campaigns = make_campaigns()
    weights = day_weights(campaigns)
    customers = make_customers()
    raw_orders, latent = make_orders(customers, weights, campaigns)

    n_o = len(raw_orders)
    cust = customers.iloc[raw_orders.customer_idx].reset_index(drop=True)
    orders = pd.DataFrame({
        "order_id": [f"KB{i:06d}" for i in range(100001, 100001 + n_o)],
        "customer_id": cust.customer_id.to_numpy(),
        "order_datetime": raw_orders.order_datetime.to_numpy(),
    })
    # channel: mostly the customer's signup channel, app share grows over time
    pref = cust.signup_channel.to_numpy()
    other = rng.choice(["Web", "App", "WhatsApp"], n_o, p=[0.4, 0.4, 0.2])
    orders["channel"] = np.where(rng.random(n_o) < 0.8, pref, other)
    prov = cust.province.to_numpy()
    can_pickup = np.isin(prov, list(PICKUP_PROVINCES))
    orders["delivery_method"] = np.where(can_pickup & (rng.random(n_o) < 0.28),
                                         "Pickup Point", "Home Delivery")
    orders["province"] = prov

    # campaign attribution: orders during a campaign window, ~35% attributed
    orders["campaign_id"] = None
    od = pd.to_datetime(orders.order_datetime).dt.normalize()
    for _, c in campaigns.iterrows():
        m = (od >= c.start_date) & (od <= c.end_date) & (rng.random(n_o) < 0.35)
        orders.loc[m, "campaign_id"] = c.campaign_id

    # ---- order items ----
    n_lines = rng.geometric(0.42, n_o)
    n_lines = np.clip(n_lines, 1, 7)
    item_order = np.repeat(np.arange(n_o), n_lines)
    line_no = np.concatenate([np.arange(1, k + 1) for k in n_lines])
    months = pd.DatetimeIndex(orders.order_datetime).month.to_numpy()[item_order]
    iprov = prov[item_order]
    cats = list(CATALOGUE)
    base = np.array([CATALOGUE[c][0] for c in cats])
    cat_choice = np.empty(len(item_order), dtype=object)
    # category probabilities vary by month and province
    for mth in range(1, 13):
        for pv in PROVINCES:
            mask = (months == mth) & (iprov == pv)
            if not mask.any():
                continue
            p = base.copy()
            if mth in (1, 5, 9):
                p[cats.index("Stationery")] *= 2.6
                p[cats.index("Fashion")] *= 1.3  # school uniforms
            if mth == 12:
                p[cats.index("Electronics")] *= 1.6
                p[cats.index("Fashion")] *= 1.5
                p[cats.index("Home & Kitchen")] *= 1.3
            if pv == "Copperbelt":
                p[cats.index("Electronics")] *= 1.45
            if PROVINCES[pv][2] > 0.6:
                p[cats.index("Electronics")] *= 1.25  # solar demand
                p[cats.index("Groceries")] *= 0.85
            cat_choice[mask] = rng.choice(cats, mask.sum(), p=p / p.sum())
    # product within category: Zipf-like popularity
    prod_by_cat = {c: products[products.category == c] for c in cats}
    pop = {}
    for c, df in prod_by_cat.items():
        r = rng.permutation(len(df)) + 1
        w = 1 / r ** 0.9
        pop[c] = w / w.sum()
    product_id = np.empty(len(item_order), dtype=object)
    for c in cats:
        m = cat_choice == c
        product_id[m] = rng.choice(prod_by_cat[c].product_id.to_numpy(), m.sum(), p=pop[c])
    pinfo = products.set_index("product_id").loc[product_id]
    qty = np.where(pinfo.category.isin(["Groceries", "Household", "Stationery", "Baby & Kids"]),
                   1 + rng.poisson(0.9, len(product_id)), 1 + rng.poisson(0.12, len(product_id)))
    qty = np.where(pinfo.category == "Electronics", 1, qty)
    otime = pd.DatetimeIndex(orders.order_datetime)[item_order]
    years_from_2025 = ((otime - pd.Timestamp("2025-07-01")).days / 365.25).to_numpy()
    infl = (1.09) ** years_from_2025  # ~9% annual price inflation; list price = 2025 price
    unit_price = np.round(pinfo.list_price_zmw.to_numpy() * infl, 2)
    items = pd.DataFrame({"order_id": orders.order_id.to_numpy()[item_order], "line_no": line_no,
                          "product_id": product_id, "quantity": qty,
                          "unit_price_zmw": unit_price})
    items["_line_total"] = items.quantity * items.unit_price_zmw
    subtotal = items.groupby("order_id", sort=False)["_line_total"].sum().reindex(orders.order_id).to_numpy()

    # ---- discounts and fees ----
    has_campaign = orders.campaign_id.notna().to_numpy()
    disc_rate = np.where(has_campaign, rng.choice([0.05, 0.10, 0.15], n_o, p=[0.4, 0.4, 0.2]),
                         np.where(rng.random(n_o) < 0.06, 0.05, 0.0))
    orders["discount_zmw"] = money(subtotal * disc_rate)
    remote_o = np.array([PROVINCES[p][2] for p in prov])
    home = orders.delivery_method.to_numpy() == "Home Delivery"
    fee = np.round(35 + 120 * remote_o + rng.normal(0, 3, n_o))
    fee = np.where(subtotal >= 1000, 0, fee)
    orders["delivery_fee_zmw"] = money(np.where(home, fee, 0))

    # ---- status ----
    status = np.where(rng.random(n_o) < 0.045, "Cancelled", "Completed")
    recent = pd.DatetimeIndex(orders.order_datetime) >= pd.Timestamp("2025-12-29")
    status = np.where(recent & (status == "Completed"), "Processing", status)
    orders["status"] = status
    orders["order_datetime"] = pd.DatetimeIndex(orders.order_datetime).strftime("%Y-%m-%d %H:%M:%S")
    total = money(subtotal - orders.discount_zmw.to_numpy() + orders.delivery_fee_zmw.to_numpy())

    # ---- payments (with hidden fraud truth for Chapter 10's Bayes example) ----
    method = rng.choice(PAY_METHODS, n_o, p=PAY_P)
    is_fraud = (rng.random(n_o) < 0.005) & (method != "Cash on Delivery")
    flag = np.where(is_fraud, rng.random(n_o) < 0.90, rng.random(n_o) < 0.03)
    flag = flag & (method != "Cash on Delivery")
    pay_status = np.where(status == "Cancelled",
                          np.where(rng.random(n_o) < 0.6, "Failed", "Reversed"),
                          np.where(status == "Processing", "Pending", "Successful"))
    paid_at = pd.DatetimeIndex(orders.order_datetime) + pd.to_timedelta(
        np.where(method == "Cash on Delivery", rng.integers(6, 96, n_o) * 3600,
                 rng.integers(10, 900, n_o)), "s")
    payments = pd.DataFrame({
        "payment_id": [f"PAY{i:07d}" for i in range(1, n_o + 1)],
        "order_id": orders.order_id, "method": method, "amount_zmw": total,
        "status": pay_status, "paid_at": paid_at.strftime("%Y-%m-%d %H:%M:%S"),
        "fraud_flag": flag.astype(int)})
    payments.loc[payments.status == "Pending", "paid_at"] = None

    # ---- deliveries ----
    dmask = home & (status != "Cancelled")
    did = np.where(dmask)[0]
    dprov = prov[did]
    sla = np.array([PROVINCES[p][3] for p in dprov])
    rem = np.array([PROVINCES[p][2] for p in dprov])
    lo_hi = np.array([BASE_DISTANCE[p] for p in dprov])
    dist = np.round(lo_hi[:, 0] + rng.random(len(did)) * (lo_hi[:, 1] - lo_hi[:, 0]), 1)
    dispatch = pd.DatetimeIndex(orders.order_datetime.to_numpy()[did]) + pd.to_timedelta(
        rng.integers(1, 9, len(did)), "h")
    month_d = dispatch.month
    festive = np.isin(month_d, [12]).astype(float)
    dur_h = sla * (0.50 + 0.10 * rem) * np.exp(rng.normal(0, 0.35 + 0.25 * rem, len(did))) * (1 + 0.18 * festive)
    delivered = dispatch + pd.to_timedelta(np.round(dur_h * 60), "m")
    courier = np.where(np.isin(dprov, ["Lusaka", "Copperbelt"]),
                       rng.choice(COURIERS, len(did), p=[0.35, 0.25, 0.40]),
                       rng.choice(COURIERS, len(did), p=[0.55, 0.45, 0.0]))
    total_h = (delivered - pd.DatetimeIndex(orders.order_datetime.to_numpy()[did])).total_seconds() / 3600
    deliveries = pd.DataFrame({
        "order_id": orders.order_id.to_numpy()[did], "courier": courier,
        "dispatched_at": dispatch.strftime("%Y-%m-%d %H:%M:%S"),
        "delivered_at": delivered.strftime("%Y-%m-%d %H:%M:%S"),
        "distance_km": dist, "delayed_flag": (total_h > sla).astype(int)})
    undelivered = delivered > pd.Timestamp("2025-12-31 23:59:59")
    deliveries.loc[undelivered, "delivered_at"] = None
    deliveries.loc[undelivered, "delayed_flag"] = 0

    # ---- returns ----
    comp_orders = set(orders.order_id[status == "Completed"])
    it = items[items.order_id.isin(comp_orders)].merge(
        products[["product_id", "category"]], on="product_id")
    ret_p = it.category.map({c: CATALOGUE[c][1] for c in cats}).to_numpy() * 0.043
    delayed_set = set(deliveries.order_id[deliveries.delayed_flag == 1])
    ret_p = ret_p * np.where(it.order_id.isin(delayed_set), 1.6, 1.0)
    ret = it[rng.random(len(it)) < ret_p].copy()
    reasons = ["Damaged on arrival", "Wrong item sent", "Not as described", "Changed mind",
               "Late delivery", "Wrong size"]
    def reason_for(cat, late):
        p = np.array([0.22, 0.14, 0.24, 0.20, 0.10, 0.10])
        if cat != "Fashion":
            p[5] = 0.01
        if late:
            p[4] *= 3
        return rng.choice(reasons, p=p / p.sum())
    ret["reason"] = [reason_for(c, o in delayed_set) for c, o in zip(ret.category, ret.order_id)]
    deliv_at = deliveries.set_index("order_id").delivered_at
    order_at = orders.set_index("order_id").order_datetime
    base_t = pd.to_datetime(ret.order_id.map(deliv_at).fillna(ret.order_id.map(order_at)))
    ret_at = base_t + pd.to_timedelta(rng.integers(1, 15, len(ret)), "D")
    ret = ret[ret_at <= pd.Timestamp("2025-12-31 23:59")]
    ret_at = ret_at[ret_at <= pd.Timestamp("2025-12-31 23:59")]
    returns = pd.DataFrame({
        "return_id": [f"R{i:05d}" for i in range(1, len(ret) + 1)],
        "order_id": ret.order_id.to_numpy(), "product_id": ret.product_id.to_numpy(),
        "reason": ret.reason.to_numpy(),
        "refund_zmw": money(ret.quantity * ret.unit_price_zmw).tolist(),
        "returned_at": pd.DatetimeIndex(ret_at).strftime("%Y-%m-%d").tolist()})

    # ---- reviews ----
    reviews = make_reviews(orders, items, products, deliveries, returns)

    # ---- loyalty tier from 2025 spend (as at 31 Dec 2025) ----
    op = orders[["order_id", "customer_id", "order_datetime"]].assign(total=total, st=status)
    op = op[(op.st != "Cancelled") & (op.order_datetime >= "2025-01-01")]
    spend = op.groupby("customer_id").total.sum()
    cs = customers.customer_id.map(spend).fillna(0)
    customers["loyalty_tier"] = np.select([cs >= 10000, cs >= 3000, cs > 0],
                                          ["Gold", "Silver", "Bronze"], "None")
    customers["signup_date"] = customers.signup_date.dt.strftime("%Y-%m-%d")

    items = items.drop(columns="_line_total")
    hidden = {"is_fraud": pd.DataFrame({"payment_id": payments.payment_id, "is_fraud": is_fraud.astype(int)}),
              "latent": latent.assign(customer_id=customers.customer_id)}
    return dict(customers=customers, products=products, suppliers=suppliers, orders=orders,
                order_items=items, payments=payments, deliveries=deliveries, returns=returns,
                campaigns=campaigns, reviews=reviews), hidden


# ---------------------------------------------------------------------------
# Reviews: template text driven by real order outcomes
# ---------------------------------------------------------------------------
POS = {
    "delivery": ["Delivery was fast, arrived the next day.", "Came earlier than expected, well done.",
                 "The driver called before arriving, very professional.",
                 "Delivered to {town} on time, no stress."],
    "quality": ["Good quality, exactly as pictured.", "The {sub} is strong and well made.",
                "Quality is better than what I find in town.", "Original product, very happy."],
    "price": ["Fair price compared to the shops.", "Good value for money.",
              "The discount made it worth it.", "Cheaper than Kamwala and no transport costs."],
    "payment": ["Paying with {pay} was smooth.", "Mobile money payment went through instantly.",
                "Easy checkout on the app."],
    "service": ["Customer care on WhatsApp answered quickly.", "Friendly staff at the pickup point.",
                "They kept me updated throughout."],
}
NEG = {
    "delivery": ["Delivery to {town} took too long.", "Waited almost a week, no updates.",
                 "Late delivery, I had to call them twice.", "The courier could not find my house."],
    "quality": ["The {sub} broke after a few days.", "Not the same as the picture.",
                "Poor quality, would not buy again.", "Packaging was damaged and the item scratched."],
    "price": ["Too expensive for what you get.", "Delivery fee is too high for {province}.",
              "Price went up since last month."],
    "payment": ["{pay} payment failed twice before it worked.", "I was charged but the order showed unpaid.",
                "Refund is taking too long."],
    "service": ["Customer care did not respond.", "Nobody at the pickup point knew about my order.",
                "Had to explain my problem three times."],
}


def make_reviews(orders, items, products, deliveries, returns):
    done = orders[orders.status == "Completed"]
    pick = done.sample(frac=0.27, random_state=SEED)
    first_items = items[items.order_id.isin(pick.order_id)].drop_duplicates("order_id")
    first_items = first_items.sample(n=min(9000, len(first_items)), random_state=SEED)
    df = first_items.merge(orders[["order_id", "customer_id", "order_datetime", "province"]], on="order_id") \
        .merge(products[["product_id", "subcategory", "category"]], on="product_id")
    delayed = set(deliveries.order_id[deliveries.delayed_flag == 1])
    returned = set(returns.order_id)
    cust_town = {}
    pay = {}
    rows = []
    for k, r in enumerate(df.itertuples(index=False), start=1):
        late = r.order_id in delayed
        ret = r.order_id in returned
        score = 4.1 - 1.3 * late - 1.6 * ret + rng.normal(0, 0.85)
        rating = int(np.clip(np.round(score), 1, 5))
        themes = rng.choice(list(POS), size=2, replace=False)
        if late:
            themes[0] = "delivery"
        if ret:
            themes[0] = "quality"
        bank = POS if rating >= 4 else NEG
        parts = []
        for i, th in enumerate(themes):
            b = bank if not (rating == 3 and i == 1) else (POS if bank is NEG else NEG)
            parts.append(rng.choice(b[th]))
        text = " ".join(parts).format(town=_town(r.province),
                                      sub=r.subcategory.lower(), province=r.province,
                                      pay=rng.choice(["Airtel Money", "MTN MoMo", "Zamtel Kwacha"]))
        if rng.random() < 0.08:
            text += rng.choice([" Zikomo!", " Natotela!", " Twalumba.", " Keep it up KB."])
        rdate = pd.Timestamp(r.order_datetime) + pd.Timedelta(days=int(rng.integers(2, 20)))
        if rdate > END:
            continue
        rows.append({"review_id": f"RV{k:05d}", "order_id": r.order_id, "product_id": r.product_id,
                     "rating": rating, "review_text": text, "review_date": rdate.date().isoformat()})
    out = pd.DataFrame(rows).sort_values("review_date", kind="stable").reset_index(drop=True)
    out["review_id"] = [f"RV{i:05d}" for i in range(1, len(out) + 1)]
    return out


def _town(p):
    t = PROVINCES[p][1]
    return t[rng.integers(len(t))]


# ---------------------------------------------------------------------------
# SQLite writer
# ---------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE suppliers (supplier_id TEXT PRIMARY KEY, supplier_name TEXT NOT NULL,
  country TEXT NOT NULL, lead_time_days INTEGER);
CREATE TABLE products (product_id TEXT PRIMARY KEY, sku TEXT UNIQUE, product_name TEXT NOT NULL,
  category TEXT NOT NULL, subcategory TEXT, brand TEXT, brand_tier TEXT,
  supplier_id TEXT REFERENCES suppliers(supplier_id), unit_cost_zmw REAL, list_price_zmw REAL,
  weight_kg REAL, imported_flag INTEGER, launch_date TEXT);
CREATE TABLE customers (customer_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT,
  gender TEXT, birth_year INTEGER, province TEXT, town TEXT, phone TEXT, signup_date TEXT,
  signup_channel TEXT, loyalty_tier TEXT);
CREATE TABLE campaigns (campaign_id TEXT PRIMARY KEY, campaign_name TEXT, channel TEXT,
  start_date TEXT, end_date TEXT, budget_zmw REAL);
CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT REFERENCES customers(customer_id),
  order_datetime TEXT NOT NULL, channel TEXT, delivery_method TEXT, province TEXT,
  campaign_id TEXT REFERENCES campaigns(campaign_id), discount_zmw REAL, delivery_fee_zmw REAL,
  status TEXT);
CREATE TABLE order_items (order_id TEXT REFERENCES orders(order_id), line_no INTEGER,
  product_id TEXT REFERENCES products(product_id), quantity INTEGER, unit_price_zmw REAL,
  PRIMARY KEY (order_id, line_no));
CREATE TABLE payments (payment_id TEXT PRIMARY KEY, order_id TEXT REFERENCES orders(order_id),
  method TEXT, amount_zmw REAL, status TEXT, paid_at TEXT, fraud_flag INTEGER);
CREATE TABLE deliveries (order_id TEXT PRIMARY KEY REFERENCES orders(order_id), courier TEXT,
  dispatched_at TEXT, delivered_at TEXT, distance_km REAL, delayed_flag INTEGER);
CREATE TABLE returns (return_id TEXT PRIMARY KEY, order_id TEXT REFERENCES orders(order_id),
  product_id TEXT REFERENCES products(product_id), reason TEXT, refund_zmw REAL, returned_at TEXT);
CREATE TABLE reviews (review_id TEXT PRIMARY KEY, order_id TEXT REFERENCES orders(order_id),
  product_id TEXT REFERENCES products(product_id), rating INTEGER, review_text TEXT,
  review_date TEXT);
CREATE INDEX ix_orders_customer ON orders(customer_id);
CREATE INDEX ix_orders_date ON orders(order_datetime);
CREATE INDEX ix_items_product ON order_items(product_id);
CREATE INDEX ix_payments_order ON payments(order_id);
"""
TABLE_ORDER = ["suppliers", "products", "customers", "campaigns", "orders", "order_items",
               "payments", "deliveries", "returns", "reviews"]


def write_sqlite(tables, path: Path):
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    for name in TABLE_ORDER:
        df = tables[name]
        cols = list(pd.read_sql(f"SELECT * FROM {name} LIMIT 0", con).columns)
        df = df[cols].astype(object).where(df[cols].notna(), None)
        con.executemany(f"INSERT INTO {name} VALUES ({','.join('?' * len(cols))})",
                        df.itertuples(index=False, name=None))
    con.commit()
    con.execute("VACUUM")
    con.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--instructor", default=None, help="folder for the hidden answer key")
    args = ap.parse_args()
    out = Path(args.out)
    tables, hidden = build()
    (out / "clean").mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        df.to_csv(out / "clean" / f"{name}.csv", index=False)
    write_sqlite(tables, out / "kwacha_basket.db")
    from make_chapter_files import make_all  # noqa: E402  (same folder)
    key = make_all(tables, hidden, out, seed=SEED)
    if args.instructor:
        ip = Path(args.instructor)
        ip.mkdir(parents=True, exist_ok=True)
        hidden["is_fraud"].to_csv(ip / "payments_fraud_truth.csv", index=False)
        hidden["latent"].to_csv(ip / "customer_latent_traits.csv", index=False)
        (ip / "answer_key.json").write_text(json.dumps(key, indent=2, default=str))
    print("Kwacha Basket data written to", out)
    for name, df in tables.items():
        print(f"  {name:<12} {len(df):>8,} rows")


if __name__ == "__main__":
    main()
