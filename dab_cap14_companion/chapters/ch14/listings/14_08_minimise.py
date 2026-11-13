PHONE = re.compile(r"(?:\+?260|0)\s?[79]\d(?:\s?\d){7}")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

def minimise(text: str) -> str:
    """Remove contact details before text leaves the company."""
    return EMAIL.sub("[email]", PHONE.sub("[phone]", text))

print(minimise("Call me on 0977 123 456 or +260 966123456, or write to grace.mwila@example.com"))

batch = (reviews[["review_id", "review_text"]].head(25)
         .assign(review_text=lambda d: d["review_text"].map(minimise))
         .rename(columns={"review_text": "text"}))
print(f"\nSent per review: {list(batch.columns)}; not sent: customer, province, date, rating")
print(f"Contact details found in the 1,000 reviews: "
      f"{reviews['review_text'].str.contains(PHONE).sum() + reviews['review_text'].str.contains(EMAIL).sum()}")
