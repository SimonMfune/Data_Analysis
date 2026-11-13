oof = cross_val_predict(model, X, y, cv=folds, method="predict_proba")[:, 1]   # every customer scored out-of-fold
audit = churn[["gender", "province"]].assign(churned=y, p=oof, flagged=oof >= best)

def group_metrics(g):
    return pd.Series({"customers": len(g), "churn_rate": g["churned"].mean(),
                      "flag_rate": g["flagged"].mean(), "AUC": roc_auc_score(g["churned"], g["p"]),
                      "recall": recall_score(g["churned"], g["flagged"]),
                      "precision": precision_score(g["churned"], g["flagged"])})

print(f"Threshold {best:.2f}, out-of-fold predictions for all {len(audit):,} customers\n")
print(audit.groupby("gender").apply(group_metrics, include_groups=False).round(3).to_string())
print()
print(audit.groupby("province").apply(group_metrics, include_groups=False)
      .sort_values("customers", ascending=False).round(3).to_string())
