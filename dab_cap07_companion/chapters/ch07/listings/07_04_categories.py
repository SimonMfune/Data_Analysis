print(customers["province"].value_counts(normalize=True).mul(100).round(1).head(5))
print(customers["age_band"].value_counts().sort_index())
