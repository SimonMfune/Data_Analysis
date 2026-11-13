# Chapter 1 — Answers

## Check Your Understanding (Section 1.4)
1. `has_app` is **qualitative** (nominal, binary). True/False are categories, even though Python can count them.
2. Age in whole years is **discrete** as recorded. Age itself is continuous; recording it in days makes the steps finer but it is still recorded discretely. Analysts usually treat age as continuous.
3. Number of shopping visits is **discrete**: a count.

## Check Your Understanding (Section 1.5)
1. `distance_km` is **ratio**: equal intervals and a true zero (0 km means no distance), so 400 km is twice 200 km.
2. No. `brand_tier` is **ordinal**; report the mode or median tier, or the share of products in each tier.
3. Celsius is an **interval** scale: 0 °C is not "no temperature", so ratios are meaningless. (In kelvin, 32 °C = 305.15 K and 16 °C = 289.15 K — about 5% warmer, not twice as hot.)

## Review questions (outline answers)
1. Ask, Prepare, Process, Analyse, Share, Act — e.g. define the repeat-purchase question; locate the orders table; remove cancelled orders; compute 90-day repeat rates; present one chart and a recommendation; decide and monitor.
2. Acting produces new results and new questions, so analysis repeats.
3. Mobile-money provider examples: transactions per agent last month (descriptive); why one district's volume fell (diagnostic); which agents will run out of float tomorrow (predictive); how much float to send to each agent (prescriptive).
4. Phone numbers are labels; adding or averaging them has no meaning.
5. `delivery_hours` is continuous; items in a basket is discrete.
6. Birth year has an arbitrary zero (interval); age has a true zero (ratio).
7. The median (or mode). Gaps between tiers are not equal, so a mean has no clear meaning.
8. Voice note: unstructured. Excel price list: structured. JSON notification: semi-structured. Photograph: unstructured.
9. Example: "For each campaign run in 2025, how many orders were attributed to it, what was the revenue per kwacha of budget, and how did it compare with the average for its channel?"
10. Any three of: minimise data extracted; pseudonymise; report aggregates; keep data in approved locations; do not paste personal data into unapproved AI tools.

## Exercise 1.2 — model answer (one of several good answers)
**Q1.** "In 2025, what percentage of home deliveries in each province arrived later than the province's promised delivery time, and how does the rate compare with Lusaka?"
- Lagging: late-delivery rate = deliveries with `delayed_flag = 1` ÷ delivered orders, per province, 2025 (tables: `deliveries`, `orders`).
- Leading: share of orders dispatched more than 8 hours after being placed, per province, per week (`deliveries.dispatched_at`, `orders.order_datetime`).

**Q2.** "Did the late-delivery rate to Western, Northern, Muchinga and Luapula provinces in December 2025 exceed their rate in October–November 2025?" (lagging: monthly late rate; leading: orders per day per courier).

**Q3.** "Among customers in provinces with a late-delivery rate above 15% in 2025, is the 90-day repeat rate lower than among customers elsewhere?" (links delivery to the business outcome; tables `deliveries`, `orders`).
