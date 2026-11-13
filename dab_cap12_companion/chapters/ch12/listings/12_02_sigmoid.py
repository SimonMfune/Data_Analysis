def sigmoid(z):
    """Turn any number (a log-odds) into a probability between 0 and 1."""
    return 1 / (1 + np.exp(-z))

for z in [-4, -2, 0, 2, 4]:
    p = sigmoid(z)
    print(f"log-odds {z:>2}  ->  odds {np.exp(z):7.3f}  ->  probability {p:.3f}")

z = np.linspace(-7, 7, 300)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(z, sigmoid(z))
ax.axhline(0.5, color="#9AA5B1", linewidth=0.8, linestyle="--")
ax.axvline(0, color="#9AA5B1", linewidth=0.8, linestyle="--")
ax.set_xlabel("Log-odds  z = b₀ + b₁·x₁ + b₂·x₂ + ...")
ax.set_ylabel("Probability of churn")
ax.set_title("The sigmoid squeezes any score into a probability between 0 and 1")
ax.set_ylim(-0.02, 1.02)
fig.savefig(FIG + "fig_12_1_sigmoid.png", dpi=200)
plt.close(fig)
