default = pd.read_csv("data/clean/customers.csv")
print(default["loyalty_tier"].value_counts(dropna=False))
print("phone dtype:", default["phone"].dtype, "  first phone:", default.loc[0, "phone"])

careful = pd.read_csv("data/clean/customers.csv", dtype={"phone": str},
                      keep_default_na=False, na_values=[""])
print(careful["loyalty_tier"].value_counts(dropna=False))
print("phone dtype:", careful["phone"].dtype, "  first phone:", careful.loc[0, "phone"])
