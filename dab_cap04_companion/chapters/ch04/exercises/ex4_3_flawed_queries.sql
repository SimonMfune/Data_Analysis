-- Exercise 4.3 — Audit five AI-generated queries.
-- Each query below was produced by an AI assistant for the question in its comment.
-- Each one runs without an error. Each one gives a wrong answer. Find the fault,
-- explain it in one or two sentences, and write a corrected query.

-- A. "What were our top five customers by revenue in 2025?"
SELECT o.customer_id, ROUND(SUM(i.quantity * i.unit_price_zmw), 2) AS revenue_zmw
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.order_datetime >= '2025-01-01' AND o.order_datetime < '2026-01-01'
GROUP BY o.customer_id
ORDER BY revenue_zmw DESC
LIMIT 5;

-- B. "How many orders did each channel receive in 2025?"
SELECT o.channel, COUNT(*) AS orders
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.order_datetime >= '2025-01-01' AND o.order_datetime < '2026-01-01'
  AND o.status <> 'Cancelled'
GROUP BY o.channel;

-- C. "How many non-cancelled orders were placed in 2025?"
SELECT COUNT(*) AS orders_2025
FROM orders
WHERE strftime('%Y', order_datetime) = 2025
  AND status <> 'Cancelled';

-- D. "What did customers pay in delivery fees on non-cancelled orders in 2025, by province?"
SELECT o.province, ROUND(SUM(o.delivery_fee_zmw), 2) AS delivery_fees_zmw
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_datetime >= '2025-01-01' AND o.order_datetime < '2026-01-01'
GROUP BY o.province
ORDER BY delivery_fees_zmw DESC;

-- E. "How many non-cancelled orders has each customer placed, including customers with none?"
SELECT c.customer_id, COUNT(o.order_id) AS orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_id
ORDER BY orders
LIMIT 5;
