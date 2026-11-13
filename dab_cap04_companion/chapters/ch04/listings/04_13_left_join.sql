SELECT COUNT(*) AS customers_with_no_orders
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
