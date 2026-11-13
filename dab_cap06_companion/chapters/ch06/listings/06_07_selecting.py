cols = ["order_id", "province", "items", "subtotal_zmw"]
print(messy[cols].iloc[:3])                          # rows by position

negative = messy["items"] < 0                        # a Boolean mask
print("Negative item counts:", negative.sum())
print(messy.loc[negative, cols].head(3))             # rows by condition

big = messy.query("subtotal_zmw > 100000")
print(big[cols])
