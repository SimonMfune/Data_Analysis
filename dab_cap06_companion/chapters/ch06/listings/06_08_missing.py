missing = messy.isna().sum()
print(missing[missing > 0])
print(f"Rows with any missing value: {messy.isna().any(axis=1).sum():,}")
