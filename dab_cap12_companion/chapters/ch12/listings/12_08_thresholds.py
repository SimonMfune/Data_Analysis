rows = []
for t in [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
    p = (proba >= t).astype(int)
    rows.append({"threshold": t, "flagged": p.sum(), "precision": precision_score(y_test, p),
                 "recall": recall_score(y_test, p), "F1": f1_score(y_test, p)})
print(pd.DataFrame(rows).round(3).to_string(index=False))
