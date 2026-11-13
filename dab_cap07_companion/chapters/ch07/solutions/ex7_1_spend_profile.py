"""Exercise 7.1 solution: spending by age band and province."""
import pandas as pd

pd.set_option("display.float_format", "{:,.0f}".format)
c = pd.read_csv("data/clean/kb_customer_demographics.csv", keep_default_na=False, na_values=[""])

for col in ["age_band", "province"]:
    table = (c.groupby(col)["total_spend_zmw"].agg(["count", "median", "mean"])
             .sort_values("median", ascending=False))
    print(table, end="\n\n")

west = c.loc[c["province"] == "Western", "total_spend_zmw"].median()
south = c.loc[c["province"] == "Southern", "total_spend_zmw"].median()
print(f"Finding 1: Southern's median (K{south:,.0f}) is {south / west:.2f}x Western's (K{west:,.0f}).")
print("Finding 2: medians rise gently with age, from K8,522 (18-24) to K10,309 (55+).")
print("Finding 3: means are about 1.55x medians in every age band, so a few heavy buyers drive averages.")
