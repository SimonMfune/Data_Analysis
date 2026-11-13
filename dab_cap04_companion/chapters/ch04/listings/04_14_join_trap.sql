-- Wrong: delivery fees are counted once per order LINE
SELECT ROUND(SUM(o.delivery_fee_zmw), 2) AS delivery_fees_wrong
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.status <> 'Cancelled';

-- Right: aggregate at the level the column belongs to
SELECT ROUND(SUM(delivery_fee_zmw), 2) AS delivery_fees_right
FROM orders
WHERE status <> 'Cancelled';
