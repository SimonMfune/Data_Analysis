p_late = deliveries["delayed_flag"].mean()
late_given = deliveries.groupby("province")["delayed_flag"].mean()
print(f"P(late) = {p_late:.3f}")
print(f"P(late | Lusaka)  = {late_given['Lusaka']:.3f}")
print(f"P(late | Western) = {late_given['Western']:.3f}")

p_western = (deliveries["province"] == "Western").mean()
print(f"\nMultiplication rule: P(Western and late) = P(Western) x P(late | Western)"
      f" = {p_western:.4f} x {late_given['Western']:.3f} = {p_western * late_given['Western']:.4f}")
print(f"Counted directly: {((deliveries['province'] == 'Western') & (deliveries['delayed_flag'] == 1)).mean():.4f}")
print(f"If lateness were independent of province: {p_western:.4f} x {p_late:.3f} = {p_western * p_late:.4f}")
