nobody = np.zeros_like(y_test)
print(f"'Nobody churns' baseline: accuracy {accuracy_score(y_test, nobody):.3f}, "
      f"recall {recall_score(y_test, nobody):.3f}")
print(f"Logistic model at 0.5:    accuracy {accuracy_score(y_test, pred):.3f}, "
      f"recall {recall_score(y_test, pred):.3f}")
