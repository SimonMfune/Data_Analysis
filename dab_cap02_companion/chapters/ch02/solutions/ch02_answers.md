# Chapter 2 — Answers

## Check Your Understanding (Section 2.5)
1. A notebook (or `# %%` cells): you are exploring and want quick feedback.
2. A script: it must run the same way every week, and could be scheduled.
3. Cells run out of order (or a cell edited and not rerun) left hidden state. Restart the kernel and run all cells from the top.

## Review questions (outline answers)
1. Sources (website orders), storage (SQLite database), analysis (pandas cleaning script), presentation (Streamlit app or dashboard).
2. SQL (or Python) to calculate it, saved so it can be rerun each month; an Excel table or dashboard to present it.
3. Manual steps are slow, error-prone and hard to audit; a mistake is easy to make and hard to find.
4. They isolate each project's package versions. A shared set means an upgrade for one project can break another.
5. When the organisation has 200 or more employees or contractors and is not using it for course-based teaching at an accredited university — or whenever IT policy says so.
6. VS Code is using a different interpreter. Select the `dab` interpreter and open a new terminal.
7. Notebook: immediate feedback; results beside code. Script: runs reproducibly top to bottom; easy to version, test and schedule.
8. Relative paths are resolved from the working directory, not the script's folder.
9. `git add` (stage), `git commit` (record a snapshot locally), `git push` (upload commits to GitHub).
10. No. It remains in the history. Revoke the key with the provider, create a new one, and update `.gitignore`.
