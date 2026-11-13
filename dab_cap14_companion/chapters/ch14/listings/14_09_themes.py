from typing import Literal

from pydantic import BaseModel, ValidationError

Theme = Literal["delivery", "price_value", "product_quality", "payment", "customer_service", "pickup_point"]

class ReviewLabel(BaseModel):
    review_id: str
    sentiment: Literal["positive", "mixed", "negative"]
    themes: list[Theme]

def theme_prompt(batch: pd.DataFrame) -> str:
    return (
        "Label each customer review below.\n"
        "For each review give: review_id (copied exactly), sentiment (positive, mixed or negative), and "
        "themes: zero or more of delivery, price_value, product_quality, payment, customer_service, "
        "pickup_point.\n"
        "Some reviews include words in Bemba, Nyanja or Tonga; treat thanks such as Natotela, Zikomo "
        "and Twalumba as positive.\n"
        "Return only JSON: a list of objects with keys review_id, sentiment, themes. No other text.\n\n"
        f"{batch.to_json(orient='records')}")

def label_batch(client, batch, retries=1):
    """Ask for labels, validate every row against the schema, and retry once on failure."""
    for attempt in range(retries + 1):
        reply = client.complete(theme_prompt(batch))
        try:
            raw = json.loads(reply.text.strip().removeprefix("```json").removesuffix("```"))
            labels = [ReviewLabel.model_validate(item) for item in raw]
            return labels, reply
        except (json.JSONDecodeError, ValidationError) as error:
            print(f"  attempt {attempt + 1} rejected: {str(error).splitlines()[0][:90]}")
    raise ValueError("No valid labels after retrying")

labels, r = label_batch(client, batch)
print(pd.DataFrame([l.model_dump() for l in labels]).head(6).to_string(index=False))

print("\nA careless reply:")
try:
    label_batch(careless, batch)
except ValueError as error:
    print(" ", error)
