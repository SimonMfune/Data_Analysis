# Chapter 4 — SQL Queries with Examples

Run everything from the repository's top folder with the `dab` environment active.

| Path | Contents |
|---|---|
| `run_sql.py` | Runs a `.sql` file (or `-q "query"`) against `data/kwacha_basket.db` and prints aligned results |
| `listings/04_01 … 04_22_*.sql` | Listings 4.1–4.22 |
| `listings/04_23_sql_to_pandas.py` | Listing 4.23 — SQL into a pandas DataFrame |
| `outputs/` | The exact output of every listing, as printed in the book |
| `exercises/ex4_1_questions.md` | Exercise 4.1 — fifteen business questions |
| `exercises/ex4_2_cohorts.md` | Exercise 4.2 — new-customer cohorts |
| `exercises/ex4_3_flawed_queries.sql` | Exercise 4.3 — five AI-generated queries to audit |
| `solutions/` | Model answers: `ex4_1/q01–q15.sql`, `ex4_1_answers.txt`, `ex4_2_cohorts.sql`, `ex4_3_answers.sql`, `ch04_answers.md` |
| `figures/ch04_figures.py` | Draws Figures 4.1 (ERD) and 4.2 (JOIN types) from the database |

Examples:
```bash
python chapters/ch04/run_sql.py chapters/ch04/listings/04_21_top_customers_2025.sql
python chapters/ch04/run_sql.py -q "SELECT COUNT(*) FROM orders WHERE status = 'Cancelled';"
```
You can also open `data/kwacha_basket.db` in DB Browser for SQLite (*Open Database Read Only*) and paste any listing into the *Execute SQL* tab.
