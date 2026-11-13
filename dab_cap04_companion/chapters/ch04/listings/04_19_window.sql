WITH province_revenue AS (
    SELECT strftime('%Y', o.order_datetime) AS year,
           o.province,
           SUM(i.quantity * i.unit_price_zmw) AS revenue_zmw
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY year, o.province
)
SELECT year,
       province,
       ROUND(revenue_zmw, 2) AS revenue_zmw,
       RANK() OVER (PARTITION BY year ORDER BY revenue_zmw DESC) AS rank_in_year
FROM province_revenue
WHERE province IN ('Lusaka', 'Copperbelt', 'Southern')
ORDER BY year, rank_in_year;
