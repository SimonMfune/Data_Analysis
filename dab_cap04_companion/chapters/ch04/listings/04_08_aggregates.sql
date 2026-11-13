SELECT COUNT(*)                  AS payments,
       ROUND(SUM(amount_zmw), 2) AS total_zmw,
       ROUND(AVG(amount_zmw), 2) AS average_zmw,
       MIN(amount_zmw)           AS smallest_zmw,
       MAX(amount_zmw)           AS largest_zmw
FROM payments
WHERE status = 'Successful';
