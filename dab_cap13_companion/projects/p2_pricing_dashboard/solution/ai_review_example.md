# AI code review (worked example)

Prompt given to the assistant, with `serving.py`, `validation.py` and the four files in `views/` attached:

> Review this Streamlit app against the checklist below. For each finding, quote the line and explain the
> risk. Checklist: (1) every user input is validated; (2) error messages are clear and do not expose
> internals; (3) no model training happens in the serving path; (4) cached objects are not modified;
> (5) business rules cannot be bypassed.

| # | Assistant's finding | How I checked | Decision |
|---|---|---|---|
| 1 | "The single-product form does not validate cost and weight." | Read `views/suggest.py`: `number_input` has `min_value` and `max_value`, so out-of-range values cannot be entered. | Rejected: not a real problem |
| 2 | "`serving.suggest` assumes all feature columns exist." | Called `suggest` with a DataFrame missing `weight_kg`: scikit-learn raised `ValueError: columns are missing` from deep inside the pipeline, with a long traceback. | Accepted: `suggest` now checks the columns first and raises a short, clear message |
| 3 | "The model may be retrained when the page reloads." | Searched every serving file for `fit(`: none. Only `train.py` fits. | Rejected: false alarm |
| 4 | "`st.cache_resource` shares one artefact between users; a page that changes it changes it for everyone." | Read every page: none assigns to the artefact. | Kept as is; added to the code-review checklist for future pages |
| 5 | "Batch upload shows raw exception text to users." | Uploaded an `.xlsx` renamed to `.csv`: the page shows only the error class name and advice to save as CSV UTF-8. | Rejected: already handled |
| 6 | "Rule 1 can be bypassed because the batch page does not call `apply_guardrails`." | Read `views/batch.py`: it calls `serving.suggest`, which applies the guardrails to every row; the test `test_never_below_cost_plus_ten_percent` covers it. | Rejected: the rule is applied in one place for every page |

Two of six findings were acted on (one fix, one checklist item). Four were wrong or already handled,
which is typical: an AI review is a list of hypotheses to check, not a list of bugs.
