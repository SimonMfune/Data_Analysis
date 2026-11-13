# Chapter 3 — Answers

## Check Your Understanding (Section 3.3)
1. SUM ignores text, so the 606 prices stored as text (such as `K1,227.84`) are left out without any warning.
2. The formula leaves the original data untouched and visible as evidence, documents exactly what was done, and repeats automatically on next month's export. Find & Replace edits data irreversibly, must be redone by hand, and can change cells you did not intend to (any K anywhere in the selection).
3. After both SUBSTITUTEs the text is ` 1 25000`: the space inside the number makes VALUE return `#VALUE!`. And even without that space, removing the comma deletes the *decimal* separator, so the result would be 125000 instead of 1250. Remove the spaces with a further SUBSTITUTE, then use NUMBERVALUE with the separators stated: `NUMBERVALUE("1250,00",",",".")`.

## Check Your Understanding (Section 3.5)
1. So that every spelling (`AIRTEL MONEY`, `airtel money`, `AirtelMoney`) reduces to one key, `airtelmoney`, that matches the lookup table.
2. The `if_not_found` value, `"Not found"`. A visible label shows exactly which rows need attention, instead of a `#N/A` error that breaks every total that depends on the column.
3. XLOOKUP still returns the correct bands: with its default linear search it does not require the limits to be sorted. (VLOOKUP's approximate match does require ascending order, and would give wrong answers.)

## Check Your Understanding (Section 3.9)
1. Refresh the PivotTable (right-click ▸ Refresh, or Data ▸ Refresh All).
2. Averaging percentages gives every line equal weight regardless of its size. A calculated field divides total margin by total revenue, weighting each line by its value.
3. The slicer's Report Connections: tick every PivotTable it should control.

## Review questions (outline answers)
1. Automatic expansion; calculated columns; structured references (also: banding, filters, Total Row).
2. `[@[Price Clean]]` is the Price Clean value in the current row; `tblTx[Line Total]` is the whole Line Total column.
3. The original data stays intact, the fix is visible and auditable, and it repeats automatically.
4. Stray leading, trailing and doubled spaces; `LEN` reveals them (and `CODE` reveals non-breaking spaces).
5. Left alignment; the green triangle "Number Stored as Text"; `ISNUMBER` returns FALSE (also: SUM ignores them).
6. `=IFS([@Fee]=0,"Free",[@Fee]<=60,"Standard",TRUE,"Remote")`
7. Looks only to the right; column referenced by number; approximate match by default.
8. An independent total that every summary must reproduce: here the Line Total sum of K1,166,904.25, checked against the Summary sheet and every PivotTable.
9. The spill range is not empty (or the formula is inside a Table). Clear the blocking cells or move the formula.
10. Any four of: start from the audience's questions; headline KPIs first; the right chart for the comparison; purposeful colour; clear labels with units, source and date; white space and alignment.
