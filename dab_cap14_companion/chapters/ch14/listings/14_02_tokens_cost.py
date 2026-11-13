reviews = pd.read_csv("data/clean/kb_reviews_sample.csv")
orders = pd.read_csv("data/clean/orders.csv")

all_reviews = "\n".join(reviews["review_text"])
print(f"1,000 reviews: {len(all_reviews):,} characters, about {estimate_tokens(all_reviews):,} tokens")
print(f"orders.csv as text: about {estimate_tokens(orders.to_csv(index=False)):,} tokens")
summary = orders.groupby("province")["delivery_fee_zmw"].agg(["count", "mean"]).round(1).to_json()
print(f"A per-province summary of orders: about {estimate_tokens(summary):,} tokens")

price_in, price_out = 1.00, 5.00           # example prices in US$ per million tokens: check your provider
tokens_in, tokens_out = estimate_tokens(all_reviews) + 500, 6_000
cost = tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out
print(f"\nOne pass over all reviews at the example prices: about US${cost:.3f}")
