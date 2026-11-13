sample = rng.choice(population, size=100, replace=False)
mean, se = sample.mean(), sample.std(ddof=1) / np.sqrt(len(sample))
t_crit = stats.t.ppf(0.975, df=len(sample) - 1)
print(f"Sample of 100 orders: mean K{mean:,.0f}, standard error K{se:,.1f}, t* = {t_crit:.3f}")
print(f"95% CI: K{mean - t_crit * se:,.0f} to K{mean + t_crit * se:,.0f}"
      f"   (population mean K{mu:,.0f})")

hits, intervals = 0, []
for _ in range(1_000):
    s = rng.choice(population, size=100, replace=False)
    m, e = s.mean(), s.std(ddof=1) / np.sqrt(100)
    lo, hi = m - t_crit * e, m + t_crit * e
    hits += lo <= mu <= hi
    intervals.append((lo, hi))
print(f"\nn = 100: {hits} of 1,000 intervals contain the population mean ({hits / 10:.1f}%)")

def coverage(n, reps=1_000):
    t_n = stats.t.ppf(0.975, df=n - 1)
    covered = 0
    for _ in range(reps):
        s = rng.choice(population, size=n, replace=False)
        half = t_n * s.std(ddof=1) / np.sqrt(n)
        covered += abs(s.mean() - mu) <= half
    return covered / reps

for n in [30, 400]:
    print(f"n = {n}: {coverage(n):.1%} of 1,000 intervals contain the population mean")

fig, ax = plt.subplots(figsize=(8, 4.2))
for i, (lo, hi) in enumerate(intervals[:50]):
    miss = not lo <= mu <= hi
    ax.plot([lo, hi], [i, i], color="#C8553D" if miss else "#0E9AA7", linewidth=2 if miss else 1.4)
ax.axvline(mu, color="#1B2A41", linestyle="--", linewidth=1)
ax.set_yticks([])
ax.grid(False)
ax.set_xlabel("95% confidence interval for the mean order value (K)")
ax.set_title("Most intervals capture the true mean; the coral ones miss it")
fig.savefig(FIG + "fig_10_6_ci_coverage.png", dpi=200)
plt.close(fig)
