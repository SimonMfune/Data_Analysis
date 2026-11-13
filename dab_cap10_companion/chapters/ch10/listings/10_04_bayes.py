base_rate = 0.005        # P(fraud): about 1 in 200 digital payments
sensitivity = 0.90       # P(flag | fraud): the system catches 90% of frauds
false_alarm = 0.03       # P(flag | genuine): it wrongly flags 3% of genuine payments

p_flag = sensitivity * base_rate + false_alarm * (1 - base_rate)     # total probability
posterior = sensitivity * base_rate / p_flag                          # Bayes' theorem
print(f"P(flag) = {p_flag:.4f}")
print(f"P(fraud | flag) = {posterior:.3f}")

per_10k = 10_000
frauds = per_10k * base_rate
print(f"\nOut of {per_10k:,} digital payments: {frauds:.0f} fraudulent, of which "
      f"{frauds * sensitivity:.0f} are flagged; {per_10k - frauds:,.0f} genuine, of which "
      f"{(per_10k - frauds) * false_alarm:.1f} are flagged")

digital = pay[pay["method"] != "Cash on Delivery"]
print(f"\nCheck against the data: {digital['fraud_flag'].sum():,} of {len(digital):,} digital "
      f"payments were flagged ({digital['fraud_flag'].mean():.4f}); the model predicts {p_flag:.4f}")
