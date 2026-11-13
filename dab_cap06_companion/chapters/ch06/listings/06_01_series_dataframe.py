prices = pd.Series([279.50, 137.00, 272.00], index=["P0002", "P0007", "P0557"], name="price_zmw")
print(prices)
print(prices["P0007"], prices.mean())

products = pd.DataFrame({
    "product_id": ["P0002", "P0007", "P0557"],
    "category": ["Groceries", "Groceries", "Stationery"],
    "price_zmw": [279.50, 137.00, 272.00],
})
print(products)
print(products.shape, list(products.columns))
