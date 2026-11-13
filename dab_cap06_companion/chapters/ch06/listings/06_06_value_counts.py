print(messy["province"].value_counts().head(12))
print("Distinct spellings:", messy["province"].nunique())
print(messy["channel"].value_counts(dropna=False))
