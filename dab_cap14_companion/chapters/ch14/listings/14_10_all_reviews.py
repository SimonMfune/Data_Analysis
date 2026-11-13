cached = get_client(cache=True)                          # reruns are free and identical
rows = []
for start in range(0, len(reviews), 25):                  # 40 batches of 25 reviews
    chunk = (reviews[["review_id", "review_text"]].iloc[start:start + 25]
             .assign(review_text=lambda d: d["review_text"].map(minimise))
             .rename(columns={"review_text": "text"}))
    batch_labels, _ = label_batch(cached, chunk)
    rows += [l.model_dump() for l in batch_labels]
labelled = reviews.merge(pd.DataFrame(rows), on="review_id", how="left")
print(f"{cached.calls} calls, {cached.input_tokens:,} input and {cached.output_tokens:,} output tokens")
print(f"Labelled {labelled['sentiment'].notna().sum():,} of {len(reviews):,} reviews")

themes = labelled.explode("themes").dropna(subset=["themes"])
share = (pd.crosstab(themes["category"], themes["themes"])
         .div(labelled["category"].value_counts(), axis=0) * 100)
print((share.round(0)).to_string())
