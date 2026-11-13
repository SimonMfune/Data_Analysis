# Exercise 4.1 — Fifteen business questions

Write one query for each question against `data/kwacha_basket.db`. Unless a question says otherwise,
"revenue" means item revenue, `SUM(quantity * unit_price_zmw)`, from orders whose status is not `'Cancelled'`.
Check your answers with `solutions/ex4_1/` (one `.sql` file per question) and `solutions/ex4_1_answers.txt`.

**Warm-up (one table)**
1. How many products are there in each category? Sort from most to fewest.
2. What are the ten most expensive products, by list price?
3. How many customers signed up through each channel?
4. How many orders placed in 2025 were cancelled?

**Aggregation and dates**
5. What was total revenue in 2024?
6. What is the average delivery distance, in km, to each province? (Join `deliveries` to `orders`.)
7. Which courier had the highest late-delivery rate among deliveries completed in 2025?
8. For each return reason, how many items were returned and how much was refunded?

**Joins**
9. What is the average review rating for each product category?
10. Which campaign has the most attributed (non-cancelled) orders, and what is its channel?
11. What was revenue by ordering channel (Web, App, WhatsApp) in 2025?
12. What were the five best-selling products by units in December 2025?
13. Which five suppliers' products generated the most revenue across all three years?

**Harder**
14. For each province, what percentage of its 2025 non-cancelled orders were paid by mobile money (Airtel Money, MTN MoMo or Zamtel Kwacha)?
15. How many customers placed at least one non-cancelled order in 2023 but none in 2025?
