SELECT CASE
           WHEN CAST(strftime('%d', order_datetime) AS INTEGER) >= 25
             OR CAST(strftime('%d', order_datetime) AS INTEGER) <= 2
           THEN 'Payday window (25th to 2nd)'
           ELSE 'Rest of month'
       END AS period,
       COUNT(*) AS orders,
       COUNT(DISTINCT date(order_datetime)) AS days,
       ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT date(order_datetime)), 1) AS orders_per_day
FROM orders
WHERE status <> 'Cancelled'
GROUP BY period;
