WITH customer_spend AS (
    SELECT o.customer_id,
           SUM(i.quantity * i.unit_price_zmw) AS spend_zmw
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.customer_id
)
SELECT CASE
           WHEN spend_zmw >= 50000 THEN '1. K50,000 and over'
           WHEN spend_zmw >= 20000 THEN '2. K20,000 to K49,999'
           WHEN spend_zmw >= 5000  THEN '3. K5,000 to K19,999'
           ELSE                         '4. Under K5,000'
       END AS spend_band,
       COUNT(*) AS customers,
       ROUND(SUM(spend_zmw), 2) AS spend_zmw
FROM customer_spend
GROUP BY spend_band
ORDER BY spend_band;
