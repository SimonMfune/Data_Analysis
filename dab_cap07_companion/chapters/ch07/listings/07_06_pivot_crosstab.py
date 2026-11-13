basket = customers.pivot_table(index="province", columns="signup_channel",
                               values="avg_basket_zmw", aggfunc="median")
print(basket.loc[["Lusaka", "Copperbelt", "Northern", "Western"]].round(0))

share = pd.crosstab(customers["age_band"], customers["top_category"], normalize="index")
print(share[["Electronics", "Groceries", "Fashion", "Baby & Kids"]].mul(100).round(1))
