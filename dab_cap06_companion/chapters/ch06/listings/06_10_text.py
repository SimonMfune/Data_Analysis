df = pd.read_csv("data/raw/kb_orders_messy.csv", dtype=str, keep_default_na=False, na_values=[""])
for col in df.columns:
    df[col] = df[col].str.strip()
before = len(df)
df = df.drop_duplicates()
print("Exact duplicates removed after stripping:", before - len(df))

print("WHATSAPP".title())                        # not what we want
channels = {"web": "Web", "app": "App", "whatsapp": "WhatsApp"}
df["channel"] = df["channel"].str.lower().map(channels)
print(df["channel"].value_counts(dropna=False))
