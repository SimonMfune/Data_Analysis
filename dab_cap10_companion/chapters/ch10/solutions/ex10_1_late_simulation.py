"""Exercise 10.1 solution: simulated late deliveries per week of 20, by province."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

plt.style.use("shared/kb.mplstyle")
rng = np.random.default_rng(2026)
d = pd.read_csv("data/clean/kb_delivery_times.csv")
rate = d.groupby("province")["delayed_flag"].mean()

weeks = pd.DataFrame({p: rng.binomial(20, rate[p], size=10_000) for p in rate.index})
result = pd.DataFrame({"late_rate": rate, "P(5+ late) simulated": (weeks >= 5).mean(),
                       "P(5+ late) binomial": [1 - stats.binom(20, r).cdf(4) for r in rate]})
print(result.sort_values("late_rate").round(3).to_string())

show = ["Lusaka", "Copperbelt", "Northern", "Western"]
fig, axes = plt.subplots(2, 2, figsize=(9, 5.4), sharex=True, sharey=True, layout="constrained")
for ax, p in zip(axes.flat, show):
    counts = weeks[p].value_counts(normalize=True).reindex(range(0, 13), fill_value=0)
    ax.bar(counts.index, counts.values, color=["#C8553D" if k >= 5 else "#0E9AA7" for k in counts.index])
    ax.set_title(f"{p}: P(5+ late) = {(weeks[p] >= 5).mean():.1%}", fontsize=10)
fig.supxlabel("Late deliveries in a week of 20")
fig.supylabel("Share of simulated weeks")
fig.suptitle("A bad week (5+ late, coral) is rare in Lusaka but common in Northern and Western",
             fontweight="bold", x=0.01, ha="left")
fig.savefig("chapters/ch10/solutions/output/ex10_1_late_weeks.png", dpi=150)
