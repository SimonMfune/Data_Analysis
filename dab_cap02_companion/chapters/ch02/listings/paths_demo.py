"""Listing 2.3 — paths_demo.py: find data files wherever the script is run from."""
from pathlib import Path

# This file lives in chapters/ch02/listings/, so the repository root
# is three folders up from it.
ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "clean"

orders_file = DATA / "orders.csv"
print("Looking for:", orders_file.relative_to(ROOT))
print("Found it?   ", orders_file.exists())
