ab = pd.read_csv("data/clean/kb_campaign_ab.csv")
summary = ab.groupby("group")["converted"].agg(contacts="count", conversions="sum", rate="mean")
print(summary.round(4))

wa, sms = summary.loc["WhatsApp"], summary.loc["SMS"]
diff = wa["rate"] - sms["rate"]
pooled = (wa["conversions"] + sms["conversions"]) / (wa["contacts"] + sms["contacts"])
se0 = np.sqrt(pooled * (1 - pooled) * (1 / wa["contacts"] + 1 / sms["contacts"]))
z = diff / se0
p_value = 2 * stats.norm.sf(abs(z))
print(f"\nDifference {diff:.4f}  z = {z:.2f}  two-sided p = {p_value:.4f}")

se1 = np.sqrt(wa["rate"] * (1 - wa["rate"]) / wa["contacts"] +
              sms["rate"] * (1 - sms["rate"]) / sms["contacts"])
print(f"95% CI for the difference: {diff - 1.96 * se1:.4f} to {diff + 1.96 * se1:.4f}")
print(f"Relative lift: {diff / sms['rate']:.1%}")

h = 2 * np.arcsin(np.sqrt(wa["rate"])) - 2 * np.arcsin(np.sqrt(sms["rate"]))
print(f"Cohen's h = {h:.3f}")

table = pd.crosstab(ab["group"], ab["converted"])
chi2, p_chi, _, _ = stats.chi2_contingency(table, correction=False)
print(f"Check with scipy chi-square test: p = {p_chi:.4f}")
