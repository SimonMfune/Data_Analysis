SELECT province,
       COUNT(*) AS orders,
       ROUND(AVG(delivery_fee_zmw), 2) AS avg_fee_zmw
FROM orders
WHERE delivery_method = 'Home Delivery'
  AND delivery_fee_zmw > 0
GROUP BY province
HAVING AVG(delivery_fee_zmw) > 100
ORDER BY avg_fee_zmw DESC;
