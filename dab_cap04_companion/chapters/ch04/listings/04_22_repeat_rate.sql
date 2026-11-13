WITH ranked AS (
    SELECT customer_id,
           order_datetime,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_datetime) AS n
    FROM orders
    WHERE status <> 'Cancelled'
),
firsts AS (
    SELECT f.customer_id,
           f.order_datetime AS first_order,
           s.order_datetime AS second_order
    FROM ranked AS f
    LEFT JOIN ranked AS s
           ON s.customer_id = f.customer_id AND s.n = 2
    WHERE f.n = 1
      AND f.order_datetime < '2025-10-01'
)
SELECT strftime('%Y', first_order) || '-Q' ||
       ((CAST(strftime('%m', first_order) AS INTEGER) + 2) / 3) AS first_quarter,
       COUNT(*) AS new_customers,
       ROUND(100.0 * SUM(julianday(second_order) - julianday(first_order) < 91)
             / COUNT(*), 1) AS repeat_90d_pct
FROM firsts
GROUP BY first_quarter
ORDER BY first_quarter;
