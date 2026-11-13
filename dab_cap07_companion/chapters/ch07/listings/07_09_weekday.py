weekday = orders["order_datetime"].dt.day_name()
order_of_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
counts = weekday.value_counts().reindex(order_of_days)
print((counts / counts.mean()).round(2))
