folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
short = ["recency_days", "orders_last_90d", "orders_last_180d", "tenure_days", "app_share"]
candidates = {
    "Five behaviour features": (Pipeline([("prepare", ColumnTransformer([("n", StandardScaler(), short)])),
                                          ("classify", LogisticRegression(max_iter=1000))]), short),
    "All features": (model, numeric + categorical),
    "All features, stronger penalty": (Pipeline([("prepare", prepare),
                                                 ("classify", LogisticRegression(C=0.05, max_iter=1000))]),
                                       numeric + categorical),
}
for name, (m, cols) in candidates.items():
    s = cross_validate(m, X_train[cols], y_train, cv=folds, scoring=["roc_auc", "average_precision"])
    print(f"{name:<32} AUC {s['test_roc_auc'].mean():.3f} ± {s['test_roc_auc'].std():.3f}   "
          f"AP {s['test_average_precision'].mean():.3f} ± {s['test_average_precision'].std():.3f}")
