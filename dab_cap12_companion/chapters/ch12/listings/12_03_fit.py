X, y = churn[numeric + categorical], churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=SEED)     # stratify keeps the churn rate equal
print(f"Churn rate: train {y_train.mean():.3f}, test {y_test.mean():.3f}")

prepare = ColumnTransformer([
    ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), numeric),
    ("categories", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical),
])
model = Pipeline([("prepare", prepare), ("classify", LogisticRegression(max_iter=1000))])
model.fit(X_train, y_train)

proba = model.predict_proba(X_test)[:, 1]                    # probability of class 1 (churn)
print(pd.DataFrame({"churned": y_test.head(6).to_numpy(), "p_churn": proba[:6].round(3),
                    "predicted": model.predict(X_test.head(6))}).to_string(index=False))
