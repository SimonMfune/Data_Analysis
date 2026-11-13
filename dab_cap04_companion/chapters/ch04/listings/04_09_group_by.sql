SELECT method,
       COUNT(*)                  AS payments,
       ROUND(SUM(amount_zmw), 2) AS total_zmw,
       ROUND(AVG(amount_zmw), 2) AS average_zmw
FROM payments
WHERE status = 'Successful'
GROUP BY method
ORDER BY total_zmw DESC;
