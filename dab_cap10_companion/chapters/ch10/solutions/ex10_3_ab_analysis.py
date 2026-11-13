"""Exercise 10.3 solution: a full analysis of the WhatsApp-versus-SMS test."""
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(2026)
ab = pd.read_csv("data/clean/kb_campaign_ab.csv")


def two_proportions(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    z = (p1 - p2) / np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    h = 2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2))
    return {"WhatsApp": p1, "SMS": p2, "diff": p1 - p2, "ci_low": p1 - p2 - 1.96 * se,
            "ci_high": p1 - p2 + 1.96 * se, "z": z, "p": 2 * stats.norm.sf(abs(z)), "h": h}


rows = {}
for outcome in ["clicked", "converted"]:
    g = ab.groupby("group")[outcome].agg(["sum", "count"])
    rows[outcome] = two_proportions(g.loc["WhatsApp", "sum"], g.loc["WhatsApp", "count"],
                                    g.loc["SMS", "sum"], g.loc["SMS", "count"])
for flag, name in [(1, "converted, existing"), (0, "converted, new")]:
    g = ab[ab["existing_customer"] == flag].groupby("group")["converted"].agg(["sum", "count"])
    rows[name] = two_proportions(g.loc["WhatsApp", "sum"], g.loc["WhatsApp", "count"],
                                 g.loc["SMS", "sum"], g.loc["SMS", "count"])
print(pd.DataFrame(rows).T.round(4).to_string())

revenue = ab.assign(rev=ab["order_value_zmw"].fillna(0))
wa = revenue.loc[revenue["group"] == "WhatsApp", "rev"].to_numpy()
sm = revenue.loc[revenue["group"] == "SMS", "rev"].to_numpy()
boot = np.array([rng.choice(wa, len(wa)).mean() - rng.choice(sm, len(sm)).mean() for _ in range(5_000)])
print(f"\nRevenue per contact: WhatsApp K{wa.mean():.2f}, SMS K{sm.mean():.2f}, "
      f"difference K{wa.mean() - sm.mean():.2f} (95% bootstrap CI K{np.percentile(boot, 2.5):.2f}"
      f" to K{np.percentile(boot, 97.5):.2f})")
print(f"Per 10,000 contacts: about K{(wa.mean() - sm.mean()) * 10_000:,.0f} more revenue with WhatsApp")
