SELECT product_name,
       unit_cost_zmw,
       list_price_zmw,
       ROUND(list_price_zmw - unit_cost_zmw, 2) AS margin_zmw,
       ROUND((list_price_zmw - unit_cost_zmw) * 100.0 / list_price_zmw, 1) AS margin_pct
FROM products
ORDER BY margin_pct DESC
LIMIT 5;
