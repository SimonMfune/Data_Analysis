SELECT o.province,
       COUNT(*)                  AS orders,
       ROUND(AVG(p.amount_zmw), 2) AS avg_order_zmw
FROM orders AS o
JOIN payments AS p ON p.order_id = o.order_id
WHERE p.status = 'Successful'
GROUP BY o.province
HAVING AVG(p.amount_zmw) > (SELECT AVG(amount_zmw)
                            FROM payments
                            WHERE status = 'Successful')
ORDER BY avg_order_zmw DESC;
