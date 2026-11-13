# Chapter 14 answers

## Check Your Understanding 14.1
1. Good: summarising computed results in words, labelling free text, drafting code. Poor: arithmetic on raw tables, anything that must be exactly right without checking, and decisions about individual people.
2. Because an LLM generates plausible text; it does not calculate. Calculations belong in pandas, where they can be checked.

## Check Your Understanding 14.2
1. About 18,900 tokens for the 1,000 reviews (75,749 characters / 4).
2. Each call is billed for input and output tokens; a 49-token summary costs a fraction of a 38,000-token raw file and leaks no customer rows.

## Check Your Understanding 14.3
1. In `.env`, which is listed in `.gitignore`; on Streamlit Community Cloud, in the app's secrets settings, read with `st.secrets`.
2. Revoke it at once in the provider's console, create a new one, and remove it from the Git history; assume it was copied.

## Check Your Understanding 14.4
1. Change `LLM_PROVIDER` (and `LLM_MODEL` and the key) in `.env`; no analysis code changes.
2. Models are replaced frequently; a name in code breaks when the model is retired, while a setting can be updated without touching code.

## Check Your Understanding 14.5
1. Role (system), context, rules, a fenced data block, and the output format.
2. It removes ambiguity: the model must quote only these numbers, and the validation code knows exactly which numbers are allowed.

## Check Your Understanding 14.6
1. Because the method compares each province with December's festive peak; January is always lower. A seasonal baseline (the same month last year, as in Exercise 14.1) would not flag it.
2. It extracts every number in the reply and checks it against the numbers in the data; 26.0, 23.8 and 19.3 appeared nowhere in the data.

## Check Your Understanding 14.7
1. A fixed list makes the output countable and comparable across batches; free-text themes would need their own clustering.
2. "store_hygiene" is not one of the allowed themes, so pydantic rejected the row and the batch was retried, then refused.

## Check Your Understanding 14.8
1. Under the Data Protection Act No. 3 of 2021, sending personal data to a provider whose servers are outside Zambia is a cross-border transfer (Part X, Sections 70-71), and sensitive personal data must be processed and stored in Zambia (Section 70(3)). Minimise first, and take advice.
2. Remove or mask names, phone numbers, emails and IDs; send only the columns the task needs.

## Exercises
- 14.1: `ex14_1_anomaly_summary.py`. Year-on-year comparison for Electronics in January 2025 flags Luapula (+539%) and Muchinga (+726%); both are small provinces where a few orders swing the percentage, which the note should say.
- 14.2: `ex14_2_themes_by_category.py` (heatmap in `output/`).
- 14.3: `ex14_3_compare_providers.py`. Without keys only the mock runs; with keys, record seconds, tokens, cost and the rubric score for each provider, and run each at least three times, because replies vary.
