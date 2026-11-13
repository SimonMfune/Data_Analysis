# AI pair-programming log (worked example, Milestone M4)

| # | What I asked | What the assistant suggested | Decision | Why | How I checked it |
|---|---|---|---|---|---|
| 1 | A function to plot a number over time by month | `df.groupby(df[date].dt.month)[value].sum()` | Rejected | Groups January 2024 with January 2025; the data spans more than a year | Plotted the loans file: 12 points instead of 23 |
| 2 | Same, using resample | `df.set_index(date).resample("M")` | Changed | `"M"` was deprecated in pandas 2.2 and raises a ValueError in pandas 3; used `"MS"` (month start), as in Chapter 7 | Ran with pandas 3: the suggestion failed, the change works |
| 3 | Make bar charts readable with many categories | Rotate x labels 45° | Rejected | Horizontal sorted bars read better (Section 8.3); folded extras into "Other" | Checked with a 34-value province column |
| 4 | Stop the chart choices breaking when a new file loads | Clear all of `st.session_state` | Changed | Clearing everything also resets the sample selector; cleared only keys starting `chart_` | AppTest: `test_switching_file_resets_chart_choices` |
| 5 | Log scale for histograms | `ax.set_xscale("log")` | Accepted, with a guard | Fails silently on zero or negative values; disabled the checkbox when any value is ≤ 0 | Fee column in clinic file contains zeros |
