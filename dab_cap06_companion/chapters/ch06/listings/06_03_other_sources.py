import sqlite3

excel = pd.read_excel("data/raw/kb_raw_transactions.xlsx", sheet_name="Transactions")
with sqlite3.connect("data/kwacha_basket.db") as con:
    deliveries = pd.read_sql("SELECT * FROM deliveries WHERE delayed_flag = 1", con)
print("Excel:", excel.shape, "  SQL:", deliveries.shape)
