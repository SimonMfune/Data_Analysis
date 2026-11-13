# Analysis report: kwacha_basket_sample: customer_churn

Generated 30 October 2026 15:19 with the AI-Enhanced Predictive Analytics Workspace.

## Data
- 2,525 rows and 20 columns after preparation.

## Model
- Logistic regression predicting **churned** from 6 features: orders_last_90d, recency_days, orders_last_180d, spend_last_180d_zmw, orders_total, returns_count.
- Trained on 1,893 rows, tested on 632.
- cv auc mean: 0.783
- cv auc sd: 0.035
- test auc: 0.774
- positive rate: 0.204

### Largest effects
| feature | coefficient | odds_ratio |
|---|---|---|
| recency_days | 0.800 | 2.226 |
| orders_last_180d | -0.384 | 0.681 |
| orders_total | -0.171 | 0.843 |
| orders_last_90d | -0.086 | 0.918 |
| spend_last_180d_zmw | -0.024 | 0.977 |
| returns_count | 0.006 | 1.006 |

## Recommendations
*AI-generated draft. Produced by a language model from the model output shown above; every figure was checked automatically against that output. Review before acting.*

1. **Act on recency days.** One standard deviation more recency_days raises the odds of churned (odds ratio 2.226). Prioritise action on this driver. (evidence: 2.226)
2. **Act on orders last 180d.** One standard deviation more orders_last_180d lowers the odds of churned (odds ratio 0.681). Prioritise action on this driver. (evidence: 0.681)
3. **Target the Q4 highest group of recency days.** Customers with recency_days from 61 to 179 average 0.458, against 0.074 in the Q1 lowest group. (evidence: 0.458, 0.074)

**Caveats.** These effects are associations in past data, not proof of cause; test any action with a controlled trial (Chapter 10).
**Confidence:** medium.
**Validation:** all figures matched the model output.

## Limitations
- Coefficients describe associations in past data, not causes.
- Results apply to data like the training data; check before using on new populations.