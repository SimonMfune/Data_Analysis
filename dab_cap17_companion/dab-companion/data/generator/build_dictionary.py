"""Writes data/DATA_DICTIONARY.md from the frozen files. Run from the repository root."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1]

CORE = {
    "customers": ("One row per registered customer.", {
        "customer_id": "Primary key (CU00001 …)", "first_name": "Given name (fictional)",
        "last_name": "Surname (fictional)", "gender": "F or M", "birth_year": "Year of birth",
        "province": "One of Zambia's ten provinces", "town": "Home town",
        "phone": "Mobile number in +260 format", "signup_date": "Date the account was created (ISO)",
        "signup_channel": "Web, App or WhatsApp",
        "loyalty_tier": "Gold (≥ K10,000 spent in 2025), Silver (≥ K3,000), Bronze (> K0), None (no 2025 purchase)"}),
    "products": ("One row per catalogue item (600 items, 8 categories).", {
        "product_id": "Primary key (P0001 …)", "sku": "Stock-keeping unit code", "product_name": "Display name",
        "category": "Groceries, Household, Electronics, Fashion, Health & Beauty, Baby & Kids, Home & Kitchen, Stationery",
        "subcategory": "Finer product group", "brand": "Fictional brand", "brand_tier": "Value, Standard or Premium",
        "supplier_id": "Foreign key to suppliers", "unit_cost_zmw": "Kwacha Basket's purchase cost (2025)",
        "list_price_zmw": "Selling price (2025)", "weight_kg": "Shipping weight",
        "imported_flag": "1 if the supplier is outside Zambia", "launch_date": "Date first listed"}),
    "suppliers": ("One row per supplier.", {
        "supplier_id": "Primary key (S001 …)", "supplier_name": "Fictional company name",
        "country": "Supplier country", "lead_time_days": "Typical days from order to warehouse"}),
    "orders": ("One row per order, 1 Jan 2023 – 31 Dec 2025.", {
        "order_id": "Primary key (KB100001 …)", "customer_id": "Foreign key to customers",
        "order_datetime": "Timestamp, YYYY-MM-DD HH:MM:SS", "channel": "Web, App or WhatsApp",
        "delivery_method": "Home Delivery or Pickup Point (Lusaka, Kitwe, Ndola, Livingstone)",
        "province": "Delivery province", "campaign_id": "Foreign key to campaigns if attributed, else empty",
        "discount_zmw": "Discount applied to the order", "delivery_fee_zmw": "Fee charged (free over K1,000)",
        "status": "Completed, Cancelled or Processing (last days of 2025)"}),
    "order_items": ("One row per order line.", {
        "order_id": "Foreign key to orders", "line_no": "Line number within the order",
        "product_id": "Foreign key to products", "quantity": "Units bought",
        "unit_price_zmw": "Price charged per unit at the time of the order (prices rise ~9% a year)"}),
    "payments": ("One payment per order.", {
        "payment_id": "Primary key", "order_id": "Foreign key to orders",
        "method": "Airtel Money, MTN MoMo, Zamtel Kwacha, Card or Cash on Delivery",
        "amount_zmw": "Items total − discount + delivery fee", "status": "Successful, Failed, Reversed or Pending",
        "paid_at": "Payment timestamp (empty if pending)",
        "fraud_flag": "1 if the fraud screen flagged the payment (not proof of fraud — see Chapter 10)"}),
    "deliveries": ("One row per home-delivered, non-cancelled order.", {
        "order_id": "Primary and foreign key", "courier": "Delivery company (fictional)",
        "dispatched_at": "Left the hub", "delivered_at": "Handed to customer (empty if still in transit)",
        "distance_km": "Distance from the nearest hub",
        "delayed_flag": "1 if order-to-delivery time exceeded the province's promised hours"}),
    "returns": ("One row per returned order line.", {
        "return_id": "Primary key", "order_id": "Foreign key to orders", "product_id": "Foreign key to products",
        "reason": "Customer's stated reason", "refund_zmw": "Amount refunded", "returned_at": "Return date"}),
    "campaigns": ("One marketing campaign per month.", {
        "campaign_id": "Primary key", "campaign_name": "Theme, year and channel",
        "channel": "Facebook, WhatsApp, SMS, Google or Radio", "start_date": "First day",
        "end_date": "Last day", "budget_zmw": "Spend"}),
    "reviews": ("Product reviews left after completed orders.", {
        "review_id": "Primary key", "order_id": "Foreign key to orders", "product_id": "Foreign key to products",
        "rating": "1–5 stars", "review_text": "Free text (unstructured)", "review_date": "Date posted"}),
}

FILES = [
    ("clean/kb_customers_sample.csv", "1", "200 customers × 20 mixed-type columns, for classifying data types and measurement scales."),
    ("raw/kb_raw_transactions.xlsx", "3", "2,500 transaction lines (2025) with planted defects, plus a Products sheet for XLOOKUP."),
    ("kwacha_basket.db", "4", "The full SQLite database: all ten tables, keys and indexes."),
    ("raw/kb_orders_messy.csv", "6", "8,190-row orders export with planted defects (dates, provinces, currency text, phones, missing values, duplicates, negatives, decimal shifts)."),
    ("clean/kb_customer_demographics.csv", "7", "One row per purchasing customer with demographics and RFM-ready metrics."),
    ("clean/kb_monthly_kpis.csv", "8", "Monthly orders, units, revenue, gross margin and returns by category and province, 2023–2025."),
    ("clean/kb_delivery_times.csv", "10", "Delivered orders with delivery hours, promised hours and late flag."),
    ("clean/kb_campaign_ab.csv", "10", "WhatsApp-vs-SMS campaign experiment, 10,000 contacts, August 2025."),
    ("clean/kb_product_pricing.csv", "11, 13", "Product attributes and list prices for the pricing model."),
    ("clean/kb_customer_churn.csv", "12", "Customer features at 30 Sep 2025 (only data up to that date) and churned = no purchase in the next 90 days."),
    ("clean/kb_reviews_sample.csv", "14", "1,000 reviews with category, province and rating, for LLM summarisation."),
    ("unseen/fintech_loans.csv", "9", "Non-Kwacha test file: comma-separated, missing values."),
    ("unseen/clinic_visits.csv", "9", "Non-Kwacha test file: semicolon-delimited, DD/MM/YYYY dates."),
    ("unseen/marketing_leads.csv", "9", "Non-Kwacha test file: Latin-1 encoded."),
]


def dtype_of(s):
    k = s.dtype.kind
    return {"i": "integer", "f": "decimal", "b": "boolean"}.get(k, "text")


def main():
    out = ["# Kwacha Basket — Data Dictionary", "",
           "Kwacha Basket Ltd is a fictional Zambian online retailer. All people, companies and brands in this data are invented. "
           "All money is in Zambian kwacha (ZMW). Every file is produced by `generator/generate_data.py` with seed 2026.", "",
           "## Core tables", "",
           "Each table is in `kwacha_basket.db` and, identically, in `clean/<table>.csv`.", ""]
    for name, (desc, cols) in CORE.items():
        df = pd.read_csv(DATA / "clean" / f"{name}.csv", nrows=2000, dtype={"phone": str})
        n = sum(1 for _ in open(DATA / "clean" / f"{name}.csv", encoding="utf-8")) - 1
        out += [f"### {name}  ({n:,} rows)", "", desc, "", "| Column | Type | Description |", "|---|---|---|"]
        out += [f"| `{c}` | {dtype_of(df[c])} | {cols[c]} |" for c in df.columns]
        out.append("")
    out += ["## Chapter files", "", "| File | Chapter | Contents |", "|---|---|---|"]
    out += [f"| `{f}` | {ch} | {d} |" for f, ch, d in FILES]
    out += ["", "Column lists for the chapter files are given in the chapters that use them.", ""]
    (DATA / "DATA_DICTIONARY.md").write_text("\n".join(out))
    print("wrote DATA_DICTIONARY.md")


if __name__ == "__main__":
    main()
