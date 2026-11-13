customers = pd.read_csv("data/clean/kb_customer_demographics.csv",
                        keep_default_na=False, na_values=[""])

fig, ax = plt.subplots(figsize=(8, 4.4))
ax.scatter(customers["orders"], customers["total_spend_zmw"] / 1000,
           s=10, alpha=0.35, edgecolors="none")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Spend rises in step with the number of orders")
ax.set_xlabel("Orders per customer, 2023-2025 (log scale)")
ax.set_ylabel("Total spend (K thousand, log scale)")
ax.grid(axis="x", visible=True)
ax.xaxis.set_major_formatter("{x:,.0f}")             # 10, 100 instead of 10¹, 10²
ax.yaxis.set_major_formatter("{x:,.1f}")
fig.savefig(FIG + "fig_8_8_scatter.png", dpi=200)
plt.close(fig)
