# Chapter 4 — Answers

## Check Your Understanding (Section 4.5)
1. The number of different customers who have placed at least one order (4,288). `COUNT(customer_id)` counts every order with a customer (62,059).
2. Each province group contains many orders, so there is no single `order_id` to show. Every selected column must be grouped or aggregated. (SQLite returns an arbitrary order_id rather than an error, which makes the mistake easy to miss.)
3. Replace the HAVING condition with `HAVING COUNT(*) > 2000`. Result: Lusaka, Copperbelt, Southern, Central, Eastern and North-Western (check with `run_sql.py`).

## Review questions (outline answers)
1. A primary key uniquely identifies each row of its own table (`orders.order_id`); a foreign key holds another table's primary key (`orders.customer_id`).
2. Normalisation: the province is a fact about the customer, stored once; copying it onto every order would repeat it and risk inconsistency.
3. One product line within an order. Joining it to `orders` repeats each order once per line, so order-level amounts must not be summed after the join.
4. Any comparison with NULL is unknown, never true. Use `WHERE campaign_id IS NULL`.
5. WHERE filters rows before grouping (`status <> 'Cancelled'`); HAVING filters groups after aggregation (`HAVING COUNT(*) > 100`).
6. ORDER BY is evaluated after SELECT has created the alias; WHERE is evaluated before.
7. `SELECT p.* FROM products p LEFT JOIN order_items i ON i.product_id = p.product_id WHERE i.product_id IS NULL;`
8. Whether the new join is to a table with a finer grain (duplicating rows), and the row count before and after the join.
9. ISO text sorts year, then month, then day, the same order as time; `DD/MM/YYYY` text sorts by day first.
10. Read it against the question and business rules; reconcile with known totals and row counts; compare with an independently written query.
