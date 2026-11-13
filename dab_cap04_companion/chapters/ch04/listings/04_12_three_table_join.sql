SELECT p.category,
       COUNT(DISTINCT o.order_id)                     AS orders,
       SUM(i.quantity)                                AS units,
       ROUND(SUM(i.quantity * i.unit_price_zmw), 2)  AS item_revenue_zmw
FROM order_items AS i
JOIN orders   AS o ON o.order_id   = i.order_id
JOIN products AS p ON p.product_id = i.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY item_revenue_zmw DESC;
