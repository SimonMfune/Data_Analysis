SELECT product_name, category, list_price_zmw
FROM products
WHERE category IN ('Stationery', 'Baby & Kids')
  AND list_price_zmw BETWEEN 200 AND 400
  AND product_name LIKE '%Bags%'
ORDER BY list_price_zmw;
