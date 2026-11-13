n = 1_000_000
fraud = rng.random(n) < base_rate
flag = np.where(fraud, rng.random(n) < sensitivity, rng.random(n) < false_alarm)
print(f"Simulated payments flagged: {flag.sum():,}")
print(f"Share of flagged payments that are fraud: {fraud[flag].mean():.3f}")

for rate in [0.001, 0.005, 0.02, 0.10]:
    post = sensitivity * rate / (sensitivity * rate + false_alarm * (1 - rate))
    print(f"base rate {rate:>5.1%}  ->  P(fraud | flag) = {post:.1%}")
