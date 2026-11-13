# A deliberately poor chart: the "before" for the AI refactoring exercise
with plt.style.context("default"):
    cat2025 = kpis[kpis["year"] == 2025].groupby("category")["revenue_zmw"].sum()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.pie(cat2025, labels=cat2025.index, colors=plt.cm.jet(np.linspace(0, 1, 8)),
           explode=[0.08] * 8, shadow=True, startangle=90)
    ax.set_title("Chart 1")
    fig.savefig(FIG + "fig_8_15_baseline.png", dpi=200)
    plt.close(fig)
