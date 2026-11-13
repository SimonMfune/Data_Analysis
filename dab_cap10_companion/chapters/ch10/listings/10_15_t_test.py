buyers = ab[ab["converted"] == 1]
a = buyers.loc[buyers["group"] == "WhatsApp", "order_value_zmw"]
b = buyers.loc[buyers["group"] == "SMS", "order_value_zmw"]
t, p = stats.ttest_ind(a, b, equal_var=False)            # Welch's t-test
pooled_sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
d = (a.mean() - b.mean()) / pooled_sd
print(f"Mean order value: WhatsApp K{a.mean():,.0f} (n={len(a)}), SMS K{b.mean():,.0f} (n={len(b)})")
print(f"Welch t = {t:.2f}, p = {p:.3f}, Cohen's d = {d:.3f}")

revenue = ab["order_value_zmw"].fillna(0)
per_contact = revenue.groupby(ab["group"]).mean()
print(f"\nRevenue per contact: WhatsApp K{per_contact['WhatsApp']:.2f}, SMS K{per_contact['SMS']:.2f}")
