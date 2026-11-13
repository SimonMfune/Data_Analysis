labels = ab["group"].to_numpy()
outcome = ab["converted"].to_numpy()
observed = outcome[labels == "WhatsApp"].mean() - outcome[labels == "SMS"].mean()

diffs = np.empty(10_000)
for i in range(len(diffs)):
    shuffled = rng.permutation(labels)        # pretend the channel made no difference
    diffs[i] = outcome[shuffled == "WhatsApp"].mean() - outcome[shuffled == "SMS"].mean()
p_perm = (np.abs(diffs) >= abs(observed)).mean()
print(f"Observed difference {observed:.4f}; shuffles at least as extreme: "
      f"{(np.abs(diffs) >= abs(observed)).sum()} of 10,000;  permutation p = {p_perm:.4f}")

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.hist(diffs * 100, bins=np.arange(-2.01, 2.05, 0.08), color="#B8C2CC")   # bins match the 0.02-point steps
ax.axvline(observed * 100, color="#C8553D", linewidth=2)
ax.text(observed * 100, ax.get_ylim()[1] * 0.9, "  observed\n  difference", color="#C8553D", fontsize=9)
ax.set_xlabel("Difference in conversion rate, WhatsApp minus SMS (percentage points)")
ax.set_ylabel("Shuffles")
ax.set_title("A difference this large almost never happens when channel labels are shuffled")
fig.savefig(FIG + "fig_10_7_permutation.png", dpi=200)
plt.close(fig)
