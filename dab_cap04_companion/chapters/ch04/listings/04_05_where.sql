SELECT order_id, order_datetime, province, delivery_fee_zmw
FROM orders
WHERE province = 'Western'
  AND delivery_method = 'Home Delivery'
  AND delivery_fee_zmw = 0
ORDER BY order_datetime DESC
LIMIT 5;
