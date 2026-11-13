# Chapter 3 — Microsoft Excel for Data Analysis

| File | Use |
|---|---|
| `../../data/raw/kb_raw_transactions.xlsx` | The practice file. **Do not edit it**: save a copy into `work/` first |
| `work/` | Put your working copy here, e.g. `work/kb_transactions_work.xlsx` |
| `solutions/kb_transactions_solution.xlsx` | Model solution: cleaned Table with every formula from the chapter, Summary sheet (Table 3.4), lookups, dynamic-array formulas to type, and the expected PivotTable (Table 3.5) |
| `solutions/check_results.py` | Recomputes every expected number in pandas, independently of Excel |
| `solutions/ch03_answers.md` | Answers to Check Your Understanding and review questions |
| `figures/ch03_figures.py` | Draws Figures 3.1–3.3 from the data |

The solution workbook needs Excel for Microsoft 365 or Excel 2021+ (XLOOKUP, IFS). It recalculates when opened.
PivotTables, PivotCharts, slicers and the dashboard are left for you to build: they are the exercises.

**How the solution was verified.** Every calculated column and the Summary sheet were recalculated in
LibreOffice (with XLOOKUP replaced by the equivalent INDEX/MATCH) and checked row by row against
`check_results.py`. The XLOOKUP and dynamic-array formulas were checked separately with a second formula engine.
