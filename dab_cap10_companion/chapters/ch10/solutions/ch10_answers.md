# Chapter 10 answers

## Check Your Understanding 10.1
1. 1 - 0.179 = 0.821.
2. Because a payment can be both in Lusaka and by mobile money; adding the two probabilities counts those payments twice.

## Check Your Understanding 10.2
1. No: P(late | Western) = 0.201 is not equal to P(late) = 0.125, so lateness depends on province.
2. P(Western and late) = 0.0384 x 0.201 = 0.0077 (counted directly: 0.0077).

## Check Your Understanding 10.3
1. About 13%. Because fraud is rare, the 3% of genuine payments wrongly flagged (about 299 per 10,000) outnumber the 45 real frauds flagged.
2. It rises to about 31%: P = 0.9 x 0.005 / (0.9 x 0.005 + 0.01 x 0.995).

## Check Your Understanding 10.4
1. E[X] = 0.2 x 1 + 0.5 x 2 + 0.3 x 3 = 2.1.
2. 0.486 (none returned); P(at least one) = 1 - 0.486 = 0.514.

## Check Your Understanding 10.5
1. z = (55 - 36.4) / 8.9 = 2.09; about 2 SD above the mean.
2. Ages are skewed, so the empirical rule is approximate: 70.3% lie within 1 SD (not 68.3%) and 99.2% within 3 SD (not 99.7%).

## Check Your Understanding 10.6
1. sigma / sqrt(400) = 1,224 / 20 = about K61.
2. The CLT is about the *means* of samples; individual orders stay as skewed as ever.

## Check Your Understanding 10.7
1. If we repeated the sampling many times, about 95% of intervals built this way would contain the true mean. It does not mean a 95% chance that this particular interval contains it.
2. Order values are strongly skewed; with n = 100 the t interval captures the mean 92% of the time, and about 95% only from several hundred orders.

## Check Your Understanding 10.8
1. p = 0.0009: if the channel made no difference, a gap of 1.58 points or more would happen about 9 times in 10,000 tests.
2. Order value: no evidence of a difference (p = 0.60, d = -0.04). The revenue gain comes from more buyers, not bigger baskets.

## Exercises
- 10.1: `ex10_1_late_simulation.py`: P(5+ late of 20) is 3% in Copperbelt, 6% in Lusaka, 37-38% in Western and Northern.
- 10.2: `ex10_2_bayes_calculator.py` and `ex10_2_bayes_app.py`. Break-even base rate 3.23%.
- 10.3: `ex10_3_ab_analysis.py`. WhatsApp raises clicks by 10.2 points (h = 0.25) and conversions by 1.6 points (95% CI 0.65 to 2.51; h = 0.07); the effect holds for new customers (p = 0.006) and is borderline for existing customers (p = 0.048). Revenue per contact rises by about K10.62 (bootstrap CI K3.37 to K18.00).
  Sample recommendation: "Use WhatsApp rather than SMS for the next campaign. In a randomised test of 10,000 contacts it raised conversion from 5.2% to 6.8% (a 30% relative lift; 95% CI +0.7 to +2.5 points), with no change in order size, adding about K10.60 of revenue per contact. The gain is clearest for new customers. Re-test after three months, and compare WhatsApp's cost per message before rolling out to all customers."
