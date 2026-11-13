import sqlite3

import matplotlib
matplotlib.use("Agg")                      # draw to files; in a notebook, omit this line
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

plt.style.use("shared/kb.mplstyle")
pd.set_option("display.width", 88)
rng = np.random.default_rng(2026)          # one seeded generator: every run gives the same numbers
FIG = "chapters/ch10/figures/"

with sqlite3.connect("data/kwacha_basket.db") as con:
    pay = pd.read_sql("""SELECT p.method, p.amount_zmw, p.fraud_flag, o.province
                         FROM payments p JOIN orders o ON o.order_id = p.order_id
                         WHERE o.status <> 'Cancelled'""", con)
deliveries = pd.read_csv("data/clean/kb_delivery_times.csv")
print(len(pay), "payments;", len(deliveries), "deliveries")
