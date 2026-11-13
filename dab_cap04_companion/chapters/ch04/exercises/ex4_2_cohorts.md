# Exercise 4.2 — New-customer cohorts

A customer's *cohort* is the month of their first non-cancelled order. Using CTEs, build a table with one
row per month of 2025 showing: the number of new customers, how many of them placed a second order within
90 days (use the definition from Listing 4.22: fewer than 91 days), and that repeat rate as a percentage.
Hint: start from the `ranked` CTE in Listing 4.22. A model answer is in `solutions/ex4_2_cohorts.sql`.
