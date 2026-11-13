plt.style.use("shared/kb.mplstyle")        # the house style, explained in Section 8.8

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly.index, monthly["revenue_zmw"] / 1e6)
ax.set_title("Revenue grew every year, with a sharp peak each December")
ax.set_ylabel("Revenue (K million)")
ax.set_ylim(0, None)                       # start at zero so growth is not exaggerated
ax.xaxis.set_major_locator(mdates.YearLocator())          # one tick per year
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.margins(x=0.01)
fig.savefig(FIG + "fig_8_3_line_after.png", dpi=200)
plt.close(fig)
