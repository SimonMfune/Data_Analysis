balanced = Pipeline([("prepare", prepare),
                     ("classify", LogisticRegression(max_iter=1000, class_weight="balanced"))])
balanced.fit(X_train, y_train)
proba_bal = balanced.predict_proba(X_test)[:, 1]
pred_bal = (proba_bal >= 0.5).astype(int)
for name, p in [("Unweighted", pred), ("class_weight='balanced'", pred_bal)]:
    tn, fp, fn, tp = confusion_matrix(y_test, p).ravel()
    print(f"{name:<24} TP {tp:>3}  FP {fp:>3}  FN {fn:>3}  precision {precision_score(y_test, p):.3f}  "
          f"recall {recall_score(y_test, p):.3f}  F1 {f1_score(y_test, p):.3f}")
print(f"AUC: unweighted {roc_auc_score(y_test, proba):.3f}, balanced {roc_auc_score(y_test, proba_bal):.3f}")
