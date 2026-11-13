"""Listing 2.2 — first_look.py: a first look at Kwacha Basket's orders.

Run from the repository root:  python chapters/ch02/listings/first_look.py
"""
# %% Load the data
import pandas as pd

orders = pd.read_csv("data/clean/orders.csv", parse_dates=["order_datetime"])

# %% Summarise it
print(f"Orders: {len(orders):,}")
print(f"From {orders['order_datetime'].min():%d %B %Y} "
      f"to {orders['order_datetime'].max():%d %B %Y}")
print()
print("Orders per year:")
print(orders["order_datetime"].dt.year.value_counts().sort_index())
print()
print("Top three provinces:")
print(orders["province"].value_counts().head(3))
