SELECT c.customer_id,
       c.first_name || ' ' || c.last_name AS customer,
       c.province,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(i.quantity * i.unit_price_zmw), 2) AS revenue_zmw
FROM customers AS c
JOIN orders      AS o ON o.customer_id = c.customer_id
JOIN order_items AS i ON i.order_id    = o.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_datetime >= '2025-01-01'
  AND o.order_datetime <  '2026-01-01'
GROUP BY c.customer_id, customer, c.province
ORDER BY revenue_zmw DESC
LIMIT 10;
