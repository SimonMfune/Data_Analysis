import sqlite3

import matplotlib
matplotlib.use("Agg")                      # draw to files; in a notebook, omit this line
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pd.set_option("display.width", 88)
pd.set_option("display.float_format", "{:,.2f}".format)
FIG = "chapters/ch08/figures/"

kpis = pd.read_csv("data/clean/kb_monthly_kpis.csv")
kpis["month"] = pd.to_datetime(kpis["month"], format="%Y-%m")
monthly = kpis.groupby("month")[["units", "revenue_zmw", "gross_margin_zmw", "returns"]].sum()
print(monthly.tail(3))
