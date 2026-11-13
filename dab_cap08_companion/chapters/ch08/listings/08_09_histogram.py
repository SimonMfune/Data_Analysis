with sqlite3.connect("data/kwacha_basket.db") as con:
    values = pd.read_sql("""SELECT p.amount_zmw FROM payments p JOIN orders o
                            ON o.order_id = p.order_id WHERE o.status <> 'Cancelled'""",
                         con)["amount_zmw"]

bins = np.logspace(np.log10(values.min()), np.log10(values.max()), 50)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.hist(values, bins=bins, color="#0E9AA7")
ax.set_xscale("log")
ax.xaxis.set_major_formatter("K{x:,.0f}")
median = values.median()
ax.axvline(median, color="#1B2A41", linewidth=1.2, linestyle="--")
ax.annotate(f"Median K{median:,.0f}", xy=(median, ax.get_ylim()[1] * 0.92),
            xytext=(8, 0), textcoords="offset points", fontsize=9)
ax.set_title("Most orders are between K100 and K3,000")
ax.set_xlabel("Order value (K, log scale)")
ax.set_ylabel("Orders")
fig.savefig(FIG + "fig_8_9_histogram.png", dpi=200)
plt.close(fig)
print(f"{values.between(100, 3000).mean():.1%} of orders are between K100 and K3,000")
