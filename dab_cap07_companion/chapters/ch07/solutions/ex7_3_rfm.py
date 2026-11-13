"""Exercise 7.3 solution: RFM segmentation with recommendations."""
import pandas as pd

c = pd.read_csv("data/clean/kb_customer_demographics.csv", keep_default_na=False, na_values=[""])
rfm = c[["customer_id", "recency_days", "orders", "total_spend_zmw"]].copy()
rfm["R"] = pd.qcut(rfm["recency_days"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F"] = pd.qcut(rfm["orders"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M"] = pd.qcut(rfm["total_spend_zmw"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

def segment(r, f):
    if r >= 4 and f >= 4: return "Champions"
    if r >= 3 and f >= 3: return "Loyal"
    if r >= 4:            return "New or returning"
    if r <= 2 and f >= 4: return "At risk"
    if r <= 2 and f <= 2: return "Lost"
    return "Needs attention"

rfm["segment"] = [segment(r, f) for r, f in zip(rfm["R"], rfm["F"])]
profile = rfm.groupby("segment").agg(customers=("customer_id", "count"),
                                     median_recency=("recency_days", "median"),
                                     median_orders=("orders", "median"),
                                     spend=("total_spend_zmw", "sum"))
profile["spend_share_pct"] = profile["spend"] / profile["spend"].sum() * 100
print(profile.drop(columns="spend").sort_values("spend_share_pct", ascending=False).round(1))
rfm.to_csv("chapters/ch07/solutions/rfm_segments.csv", index=False)
