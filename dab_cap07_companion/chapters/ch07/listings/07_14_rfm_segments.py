def segment(row):
    r, f = row["R"], row["F"]
    if r >= 4 and f >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal"
    if r >= 4:
        return "New or returning"
    if r <= 2 and f >= 4:
        return "At risk"
    if r <= 2 and f <= 2:
        return "Lost"
    return "Needs attention"

rfm["segment"] = rfm.apply(segment, axis=1)
profile = (rfm.groupby("segment")
           .agg(customers=("customer_id", "count"),
                median_recency_days=("recency_days", "median"),
                median_orders=("orders", "median"),
                spend_zmw=("total_spend_zmw", "sum")))
profile["spend_share_pct"] = profile["spend_zmw"] / profile["spend_zmw"].sum() * 100
print(profile.sort_values("spend_zmw", ascending=False).drop(columns="spend_zmw").round(1))
