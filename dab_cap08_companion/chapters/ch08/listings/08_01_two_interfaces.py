# pyplot style: quick, but every call acts on "the current" figure and axes
plt.plot(monthly.index, monthly["revenue_zmw"])
plt.title("Monthly revenue")
plt.close()

# object-oriented style: name the figure and the axes, then call their methods
fig, ax = plt.subplots()
ax.plot(monthly.index, monthly["revenue_zmw"])
ax.set_title("Monthly revenue")
print(type(fig).__name__, type(ax).__name__)
print(len(fig.axes), "axes in this figure")
plt.close(fig)
