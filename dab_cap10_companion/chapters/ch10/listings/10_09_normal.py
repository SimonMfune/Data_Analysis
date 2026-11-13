N = stats.norm(loc=100, scale=15)
for k in [1, 2, 3]:
    print(f"Normal: P(within {k} SD) = {N.cdf(100 + 15 * k) - N.cdf(100 - 15 * k):.4f}")

z = (45 - 36.4) / 8.9
print(f"\nA 45-year-old customer: z = (45 - 36.4) / 8.9 = {z:.2f}")

customers = pd.read_csv("data/clean/kb_customer_demographics.csv")
age = customers["age"]
within = [((age - age.mean()).abs() <= k * age.std()).mean() for k in [1, 2, 3]]
print("Customer ages within 1, 2, 3 SD:", [f"{w:.3f}" for w in within], f" skew {age.skew():.2f}")

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.hist(age, bins=np.arange(17.5, 71.5, 1), density=True, color="#B8C2CC", label="Customer ages")
x = np.linspace(15, 72, 300)
ax.plot(x, stats.norm(age.mean(), age.std()).pdf(x), label="Normal with the same mean and SD")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Density")
ax.set_title("Customer ages are close to Normal in the middle, but skewed to the right")
ax.legend()
fig.savefig(FIG + "fig_10_3_normal.png", dpi=200)
plt.close(fig)
