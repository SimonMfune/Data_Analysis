WITH monthly AS (
    SELECT strftime('%Y-%m', o.order_datetime) AS month,
           SUM(i.quantity * i.unit_price_zmw) AS revenue_zmw
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    WHERE o.status <> 'Cancelled'
      AND o.order_datetime >= '2025-01-01'
    GROUP BY month
)
SELECT month,
       ROUND(revenue_zmw, 2) AS revenue_zmw,
       ROUND(SUM(revenue_zmw) OVER (ORDER BY month), 2) AS year_to_date_zmw
FROM monthly
ORDER BY month;
