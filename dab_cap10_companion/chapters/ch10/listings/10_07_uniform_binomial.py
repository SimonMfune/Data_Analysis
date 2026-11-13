slot = rng.uniform(8, 17, size=10_000)        # a delivery promised "between 08:00 and 17:00"
print(f"Uniform(8, 17): P(before noon) = {(12 - 8) / (17 - 8):.3f}; "
      f"simulated {(slot < 12).mean():.3f}")

with sqlite3.connect("data/kwacha_basket.db") as con:
    returned = pd.read_sql("SELECT COUNT(DISTINCT order_id) AS n FROM returns", con)["n"][0]
p_return = returned / len(lines)
print(f"\nP(an order has a return) = {returned:,} / {len(lines):,} = {p_return:.4f}")

n_route = 20                                   # orders on one courier route
X = stats.binom(n_route, p_return)
print(f"Binomial(20, {p_return:.3f}): P(0) = {X.pmf(0):.3f}, P(1) = {X.pmf(1):.3f}, "
      f"P(2 or more) = {1 - X.cdf(1):.3f}, mean = {X.mean():.2f}")
sim = rng.binomial(n_route, p_return, size=100_000)
print(f"Simulated: P(0) = {(sim == 0).mean():.3f}, P(1) = {(sim == 1).mean():.3f}, "
      f"P(2 or more) = {(sim >= 2).mean():.3f}")

k = np.arange(0, 6)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.bar(k - 0.2, X.pmf(k), width=0.4, label="Binomial formula")
ax.bar(k + 0.2, [(sim == i).mean() for i in k], width=0.4, label="100,000 simulated routes")
ax.set_xticks(k)
ax.set_xlabel("Orders with a return, out of 20")
ax.set_ylabel("Probability")
ax.set_title("On most routes no order is returned; two or more is rare")
ax.legend()
fig.savefig(FIG + "fig_10_2_binomial.png", dpi=200)
plt.close(fig)
