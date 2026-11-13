SELECT strftime('%Y-%m', order_datetime) AS month,
       COUNT(*) AS orders
FROM orders
WHERE status <> 'Cancelled'
  AND order_datetime >= '2025-01-01'
GROUP BY month
ORDER BY month;
