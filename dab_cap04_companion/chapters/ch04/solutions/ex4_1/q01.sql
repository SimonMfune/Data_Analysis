SELECT category, COUNT(*) AS products
FROM products
GROUP BY category
ORDER BY products DESC;
