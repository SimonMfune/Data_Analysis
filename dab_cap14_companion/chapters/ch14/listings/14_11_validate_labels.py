ids_ok = set(labelled["review_id"]) == set(pd.DataFrame(rows)["review_id"])
print(f"Every returned review_id exists and none is missing: {ids_ok}")

expected = labelled["rating"].map({1: "negative", 2: "negative", 3: "mixed", 4: "positive", 5: "positive"})
agree = (labelled["sentiment"] == expected).mean()
print(f"Sentiment agrees with the star rating for {agree:.1%} of reviews")
print(pd.crosstab(labelled["rating"], labelled["sentiment"]).to_string())

sample = labelled.sample(20, random_state=2026)[["review_id", "rating", "sentiment", "themes", "review_text"]]
sample.to_csv("chapters/ch14/outputs/human_check_sample.csv", index=False)
print("\n20 random reviews saved to outputs/human_check_sample.csv for a person to check")
