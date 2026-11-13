SELECT product_name,
       category,
       list_price_zmw AS price
FROM products
ORDER BY price DESC
LIMIT 5;
