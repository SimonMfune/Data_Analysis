# Chapter 7 answers

## Check Your Understanding 7.1
1. The mean (K14,549) is pulled up by a long right tail of heavy buyers; the median (K9,320) is the typical customer. Report the median, mention the mean.
2. Skew 2.38 means a long right tail. Use the median and IQR, and consider a log scale for charts.

## Check Your Understanding 7.2
1. `count` counts non-missing values in that column, so use a column with no gaps (customer_id) to count rows per group.
2. `normalize="index"` makes each row sum to 1, so you compare category mix *within* each age band, independent of band size.

## Check Your Understanding 7.3
1. Because the windows contain different numbers of calendar days, raw order counts would favour the longer window. Divide by days.
2. Orders and revenue per day both rise; December 2025 revenue is 1.99x the other 2025 months, and orders are 3,503 against February's 1,696.

## Check Your Understanding 7.4
1. The IQR rule flags 4,432 orders (7.5%); |z| > 3 flags 1,399. The z rule uses a standard deviation that the outliers themselves inflate.
2. Keep them: they are real, valid orders. Capping would understate revenue.

## Check Your Understanding 7.5
1. Order count. Customers who order more have more chances to return something and spend more.
2. Use a rate (returns per order) and compare customers with similar order counts.

## Exercises
- 7.1: `solutions/ex7_1_spend_profile.py`
- 7.2: `solutions/ex7_2_iqr_audit.py`
- 7.3: `solutions/ex7_3_rfm.py` (segment counts: Champions 999, Lost 981, Loyal 836, Needs attention 693, New or returning 417, At risk 344)

Sample recommendations for 7.3:
1. **At risk (344 customers, 11.6% of spend, median 366 days since last order):** personal WhatsApp win-back offer timed for the payday window.
2. **Champions (999, 51.2% of spend):** early access to December stock; protect, do not discount.
3. **New or returning (417, median 4 orders):** a second-order incentive within 90 days, the window where repeat behaviour is set.
