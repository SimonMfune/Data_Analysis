# Kwacha Basket — Data Dictionary

Kwacha Basket Ltd is a fictional Zambian online retailer. All people, companies and brands in this data are invented. All money is in Zambian kwacha (ZMW). Every file is produced by `generator/generate_data.py` with seed 2026.

## Core tables

Each table is in `kwacha_basket.db` and, identically, in `clean/<table>.csv`.

### customers  (5,000 rows)

One row per registered customer.

| Column | Type | Description |
|---|---|---|
| `customer_id` | text | Primary key (CU00001 …) |
| `first_name` | text | Given name (fictional) |
| `last_name` | text | Surname (fictional) |
| `gender` | text | F or M |
| `birth_year` | integer | Year of birth |
| `province` | text | One of Zambia's ten provinces |
| `town` | text | Home town |
| `phone` | text | Mobile number in +260 format |
| `signup_date` | text | Date the account was created (ISO) |
| `signup_channel` | text | Web, App or WhatsApp |
| `loyalty_tier` | text | Gold (≥ K10,000 spent in 2025), Silver (≥ K3,000), Bronze (> K0), None (no 2025 purchase) |

### products  (600 rows)

One row per catalogue item (600 items, 8 categories).

| Column | Type | Description |
|---|---|---|
| `product_id` | text | Primary key (P0001 …) |
| `sku` | text | Stock-keeping unit code |
| `product_name` | text | Display name |
| `category` | text | Groceries, Household, Electronics, Fashion, Health & Beauty, Baby & Kids, Home & Kitchen, Stationery |
| `subcategory` | text | Finer product group |
| `brand` | text | Fictional brand |
| `brand_tier` | text | Value, Standard or Premium |
| `supplier_id` | text | Foreign key to suppliers |
| `unit_cost_zmw` | decimal | Kwacha Basket's purchase cost (2025) |
| `list_price_zmw` | decimal | Selling price (2025) |
| `weight_kg` | decimal | Shipping weight |
| `imported_flag` | integer | 1 if the supplier is outside Zambia |
| `launch_date` | text | Date first listed |

### suppliers  (40 rows)

One row per supplier.

| Column | Type | Description |
|---|---|---|
| `supplier_id` | text | Primary key (S001 …) |
| `supplier_name` | text | Fictional company name |
| `country` | text | Supplier country |
| `lead_time_days` | integer | Typical days from order to warehouse |

### orders  (62,059 rows)

One row per order, 1 Jan 2023 – 31 Dec 2025.

| Column | Type | Description |
|---|---|---|
| `order_id` | text | Primary key (KB100001 …) |
| `customer_id` | text | Foreign key to customers |
| `order_datetime` | text | Timestamp, YYYY-MM-DD HH:MM:SS |
| `channel` | text | Web, App or WhatsApp |
| `delivery_method` | text | Home Delivery or Pickup Point (Lusaka, Kitwe, Ndola, Livingstone) |
| `province` | text | Delivery province |
| `campaign_id` | text | Foreign key to campaigns if attributed, else empty |
| `discount_zmw` | decimal | Discount applied to the order |
| `delivery_fee_zmw` | decimal | Fee charged (free over K1,000) |
| `status` | text | Completed, Cancelled or Processing (last days of 2025) |

### order_items  (143,749 rows)

One row per order line.

| Column | Type | Description |
|---|---|---|
| `order_id` | text | Foreign key to orders |
| `line_no` | integer | Line number within the order |
| `product_id` | text | Foreign key to products |
| `quantity` | integer | Units bought |
| `unit_price_zmw` | decimal | Price charged per unit at the time of the order (prices rise ~9% a year) |

### payments  (62,059 rows)

One payment per order.

| Column | Type | Description |
|---|---|---|
| `payment_id` | text | Primary key |
| `order_id` | text | Foreign key to orders |
| `method` | text | Airtel Money, MTN MoMo, Zamtel Kwacha, Card or Cash on Delivery |
| `amount_zmw` | decimal | Items total − discount + delivery fee |
| `status` | text | Successful, Failed, Reversed or Pending |
| `paid_at` | text | Payment timestamp (empty if pending) |
| `fraud_flag` | integer | 1 if the fraud screen flagged the payment (not proof of fraud — see Chapter 10) |

### deliveries  (48,053 rows)

One row per home-delivered, non-cancelled order.

| Column | Type | Description |
|---|---|---|
| `order_id` | text | Primary and foreign key |
| `courier` | text | Delivery company (fictional) |
| `dispatched_at` | text | Left the hub |
| `delivered_at` | text | Handed to customer (empty if still in transit) |
| `distance_km` | decimal | Distance from the nearest hub |
| `delayed_flag` | integer | 1 if order-to-delivery time exceeded the province's promised hours |

### returns  (2,136 rows)

One row per returned order line.

| Column | Type | Description |
|---|---|---|
| `return_id` | text | Primary key |
| `order_id` | text | Foreign key to orders |
| `product_id` | text | Foreign key to products |
| `reason` | text | Customer's stated reason |
| `refund_zmw` | decimal | Amount refunded |
| `returned_at` | text | Return date |

### campaigns  (36 rows)

One marketing campaign per month.

| Column | Type | Description |
|---|---|---|
| `campaign_id` | text | Primary key |
| `campaign_name` | text | Theme, year and channel |
| `channel` | text | Facebook, WhatsApp, SMS, Google or Radio |
| `start_date` | text | First day |
| `end_date` | text | Last day |
| `budget_zmw` | decimal | Spend |

### reviews  (8,867 rows)

Product reviews left after completed orders.

| Column | Type | Description |
|---|---|---|
| `review_id` | text | Primary key |
| `order_id` | text | Foreign key to orders |
| `product_id` | text | Foreign key to products |
| `rating` | integer | 1–5 stars |
| `review_text` | text | Free text (unstructured) |
| `review_date` | text | Date posted |

## Chapter files

| File | Chapter | Contents |
|---|---|---|
| `clean/kb_customers_sample.csv` | 1 | 200 customers × 20 mixed-type columns, for classifying data types and measurement scales. |
| `raw/kb_raw_transactions.xlsx` | 3 | 2,500 transaction lines (2025) with planted defects, plus a Products sheet for XLOOKUP. |
| `kwacha_basket.db` | 4 | The full SQLite database: all ten tables, keys and indexes. |
| `raw/kb_orders_messy.csv` | 6 | 8,190-row orders export with planted defects (dates, provinces, currency text, phones, missing values, duplicates, negatives, decimal shifts). |
| `clean/kb_customer_demographics.csv` | 7 | One row per purchasing customer with demographics and RFM-ready metrics. |
| `clean/kb_monthly_kpis.csv` | 8 | Monthly orders, units, revenue, gross margin and returns by category and province, 2023–2025. |
| `clean/kb_delivery_times.csv` | 10 | Delivered orders with delivery hours, promised hours and late flag. |
| `clean/kb_campaign_ab.csv` | 10 | WhatsApp-vs-SMS campaign experiment, 10,000 contacts, August 2025. |
| `clean/kb_product_pricing.csv` | 11, 13 | Product attributes and list prices for the pricing model. |
| `clean/kb_customer_churn.csv` | 12 | Customer features at 30 Sep 2025 (only data up to that date) and churned = no purchase in the next 90 days. |
| `clean/kb_reviews_sample.csv` | 14 | 1,000 reviews with category, province and rating, for LLM summarisation. |
| `unseen/fintech_loans.csv` | 9 | Non-Kwacha test file: comma-separated, missing values. |
| `unseen/clinic_visits.csv` | 9 | Non-Kwacha test file: semicolon-delimited, DD/MM/YYYY dates. |
| `unseen/marketing_leads.csv` | 9 | Non-Kwacha test file: Latin-1 encoded. |

Column lists for the chapter files are given in the chapters that use them.
