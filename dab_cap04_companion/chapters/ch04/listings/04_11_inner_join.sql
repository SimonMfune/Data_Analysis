SELECT o.order_id,
       o.order_datetime,
       c.first_name || ' ' || c.last_name AS customer,
       c.province,
       o.status
FROM orders AS o
INNER JOIN customers AS c
        ON c.customer_id = o.customer_id
ORDER BY o.order_datetime DESC
LIMIT 5;
