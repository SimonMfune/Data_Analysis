names = [n.split("__")[1] for n in model.named_steps["prepare"].get_feature_names_out()]
coef = pd.Series(model.named_steps["classify"].coef_[0], index=names)
table = pd.DataFrame({"coefficient": coef, "odds_ratio": np.exp(coef)})
numeric_part = table.loc[numeric].sort_values("odds_ratio")
print("Numbers (per one standard deviation):")
print(numeric_part.round(3).to_string())
print(f"\nOne SD of recency_days = {X_train['recency_days'].std():.1f} days; "
      f"of orders_last_180d = {X_train['orders_last_180d'].std():.1f} orders")
print("\nProvinces (vs Central):")
print(table.loc[[n for n in names if n.startswith("province_")], "odds_ratio"].round(2).to_string())
