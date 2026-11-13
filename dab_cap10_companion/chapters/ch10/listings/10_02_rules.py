share = pay["method"].value_counts(normalize=True)
print(share.round(3).to_string())

mobile = ["Airtel Money", "MTN MoMo", "Zamtel Kwacha"]
p_mobile = share[mobile].sum()                    # addition rule: mutually exclusive methods
print(f"\nP(mobile money) = {p_mobile:.3f}")
print(f"P(not mobile money) = 1 - {p_mobile:.3f} = {1 - p_mobile:.3f}")   # complement rule

is_lusaka = pay["province"] == "Lusaka"
is_mobile = pay["method"].isin(mobile)
p_l, p_m, p_both = is_lusaka.mean(), is_mobile.mean(), (is_lusaka & is_mobile).mean()
print(f"\nP(Lusaka) = {p_l:.3f}, P(mobile) = {p_m:.3f}, P(both) = {p_both:.3f}")
print(f"General addition rule: P(Lusaka or mobile) = {p_l:.3f} + {p_m:.3f} - {p_both:.3f}"
      f" = {p_l + p_m - p_both:.3f}")
print(f"Counted directly:        {(is_lusaka | is_mobile).mean():.3f}")
