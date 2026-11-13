west = deliveries[deliveries["province"] == "Western"]["delayed_flag"]
p_hat, n = west.mean(), len(west)
se_p = np.sqrt(p_hat * (1 - p_hat) / n)
print(f"Western: {west.sum()} late of {n:,} = {p_hat:.3f}")
print(f"95% CI: {p_hat - 1.96 * se_p:.3f} to {p_hat + 1.96 * se_p:.3f}")

small = west.sample(50, random_state=1)
se_s = np.sqrt(small.mean() * (1 - small.mean()) / 50)
print(f"With only 50 deliveries: {small.mean():.3f}, 95% CI "
      f"{small.mean() - 1.96 * se_s:.3f} to {small.mean() + 1.96 * se_s:.3f}")
