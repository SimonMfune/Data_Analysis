false_positives = 0
for _ in range(1_000):                         # 1,000 A/A tests: both groups identical
    a_group = rng.random(5_000) < 0.05
    b_group = rng.random(5_000) < 0.05
    table = [[a_group.sum(), 5_000 - a_group.sum()], [b_group.sum(), 5_000 - b_group.sum()]]
    false_positives += stats.chi2_contingency(table, correction=False)[1] < 0.05
print(f"A/A tests with p < 0.05: {false_positives} of 1,000")

by_province = []
for prov, g in ab.groupby("province"):
    t = pd.crosstab(g["group"], g["converted"])
    by_province.append((prov, len(g), stats.chi2_contingency(t, correction=False)[1]))
res = pd.DataFrame(by_province, columns=["province", "contacts", "p"]).sort_values("p")
res["bonferroni_p"] = (res["p"] * len(res)).clip(upper=1)
print(res.round(4).to_string(index=False))
