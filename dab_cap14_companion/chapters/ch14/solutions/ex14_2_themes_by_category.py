"""Exercise 14.2 solution: validated themes for all reviews, charted by category."""
import json
import sys
from pathlib import Path
from typing import Literal

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.llm_client import get_client  # noqa: E402

plt.style.use(ROOT / "shared" / "kb.mplstyle")
THEMES = ["delivery", "price_value", "product_quality", "payment", "customer_service", "pickup_point"]


class ReviewLabel(BaseModel):
    review_id: str
    sentiment: Literal["positive", "mixed", "negative"]
    themes: list[Literal["delivery", "price_value", "product_quality", "payment",
                         "customer_service", "pickup_point"]]


reviews = pd.read_csv(ROOT / "data/clean/kb_reviews_sample.csv")
client = get_client(cache=True)
rows = []
for start in range(0, len(reviews), 25):
    batch = reviews[["review_id", "review_text"]].iloc[start:start + 25].rename(columns={"review_text": "text"})
    prompt = ("Label each review with review_id, sentiment (positive, mixed or negative) and themes from: "
              + ", ".join(THEMES) + ". Return only JSON: a list of objects.\n\n" + batch.to_json(orient="records"))
    reply = client.complete(prompt)
    rows += [ReviewLabel.model_validate(x).model_dump() for x in json.loads(reply.text)]
labels = reviews.merge(pd.DataFrame(rows), on="review_id")
long = labels.explode("themes").dropna(subset=["themes"])
share = pd.crosstab(long["category"], long["themes"]).div(labels["category"].value_counts(), axis=0) * 100
print(share.round(0).to_string())

fig, ax = plt.subplots(figsize=(9, 4.4))
im = ax.imshow(share[THEMES].to_numpy(), cmap="BuGn", vmin=0, vmax=70)
ax.set_xticks(range(len(THEMES)), [t.replace("_", " ") for t in THEMES], rotation=25, ha="right")
ax.set_yticks(range(len(share)), share.index)
for i in range(len(share)):
    for j, t in enumerate(THEMES):
        ax.text(j, i, f"{share.iloc[i][t]:.0f}", ha="center", va="center", fontsize=8)
ax.grid(False)
ax.set_title("Share of reviews mentioning each theme (%), by category")
fig.colorbar(im, ax=ax, shrink=0.8)
fig.savefig(Path(__file__).with_name("output") / "ex14_2_themes_by_category.png", dpi=150, bbox_inches="tight")
print(f"{client.calls} calls; {len(labels)} reviews labelled")
