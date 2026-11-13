# Chapter 12 answers

## Check Your Understanding 12.1
1. Classification: the target is a category (churned or not).
2. Customers who have not ordered for 91-180 days churn at 59.5%, against 8.8% for those who ordered in the last fortnight.

## Check Your Understanding 12.2
1. Log-odds 0 means odds of 1 (even), so the probability is 0.5.
2. Linear regression can predict values below 0 or above 1, which are not probabilities; the sigmoid keeps every prediction between 0 and 1.

## Check Your Understanding 12.3
1. Precision 0.603: of the 63 customers flagged, 38 really churned. Recall 0.295: of the 129 who churned, the model caught 38.
2. A model that predicts "nobody churns" is right for every stayer, 79.6% of customers, while catching no churners at all.

## Check Your Understanding 12.4
1. It weights each churner about four times as heavily as a stayer, so the model flags more customers: recall rises (0.295 → 0.643) and precision falls (0.603 → 0.444).
2. AUC measures ranking, which class weights barely change (0.775 vs 0.774); they move the probabilities and so the effect of a fixed threshold.

## Check Your Understanding 12.5
1. Odds ratio 2.25 per SD of recency: 42.5 more days since the last order multiplies the odds of churn by about 2.25, other features held constant.
2. Only 55 customers, 20 of whom churned; the estimate is very uncertain, and acting on it would treat every Muchinga customer as high-risk because of where they live.

## Check Your Understanding 12.6
1. Break-even precision = cost / (save rate × margin) = 150 / (0.30 × 1,253) ≈ 0.40.
2. Because test data used to choose the threshold would no longer be unseen; its result would be optimistic.

## Check Your Understanding 12.7
1. Recall is similar for women and men (0.37 vs 0.40), but precision is lower for women (0.55 vs 0.68): more of the vouchers sent to women go to customers who would have stayed.
2. Small groups (Muchinga, 55 customers) give very wide confidence intervals; differences that look large may be chance.

## Exercises
- 12.1: `ex12_1_churn_model.py`; see Listing 12.4 and 12.6 for the numbers.
- 12.2: `ex12_2_threshold.py`: the K80 waiver has a lower break-even precision (0.32), so the best threshold is lower (0.36), more customers are flagged (100 vs 77), and net benefit on the test set is slightly higher (K5,283 vs K4,991).
- 12.3: `ex12_3_fairness_audit.py`. Sample recommendations: (1) drop province as a feature, since the five behaviour features predict as well (Listing 12.10) and province effects rest on small groups; (2) monitor precision by gender each campaign, since the gap (0.55 vs 0.68) is near the edge of chance; (3) do not report or act on per-province metrics for provinces with fewer than about 100 customers without confidence intervals.
