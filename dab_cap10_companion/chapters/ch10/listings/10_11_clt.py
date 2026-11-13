fig, axes = plt.subplots(2, 2, figsize=(9, 5.6), layout="constrained")
for ax, n in zip(axes.flat, [1, 5, 30, 100]):
    means = rng.choice(population, size=(10_000, n)).mean(axis=1)
    ax.hist(means, bins=50, color="#0E9AA7", density=True)
    se = population.std() / np.sqrt(n)
    if n >= 30:
        x = np.linspace(means.min(), means.max(), 200)
        ax.plot(x, stats.norm(mu, se).pdf(x), color="#1B2A41", linewidth=1.2)
    ax.set_title(f"n = {n}", fontsize=10)
    ax.set_yticks([])
    ax.grid(False)
    print(f"n = {n:>3}: SD of sample means = {means.std():6.1f}   sigma / sqrt(n) = {se:6.1f}   "
          f"skew = {stats.skew(means):.2f}")
fig.supxlabel("Mean order value of the sample (K)", fontsize=10)
fig.suptitle("Means of larger samples become Normal, even though order values are skewed",
             fontweight="bold", x=0.01, ha="left")
fig.savefig(FIG + "fig_10_5_clt.png", dpi=200)
plt.close(fig)
