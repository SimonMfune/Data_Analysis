import sqlite3

import matplotlib
matplotlib.use("Agg")                      # draw to files; in a notebook, omit this line
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.width", 88)
pd.set_option("display.max_columns", 8)
pd.set_option("display.float_format", "{:,.2f}".format)
FIG = "chapters/ch07/figures/"
