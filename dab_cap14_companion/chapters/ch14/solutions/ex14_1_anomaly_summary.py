"""Exercise 14.1 solution: year-on-year anomaly statistics for one category, summarised by a model."""
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from shared.llm_client import get_client  # noqa: E402

CATEGORY, MONTH = "Electronics", "2025-01"
kpis = pd.read_csv("data/clean/kb_monthly_kpis.csv")
m = (kpis[kpis["category"] == CATEGORY]
     .pivot_table(index="month", columns="province", values="revenue_zmw", aggfunc="sum").fillna(0))
year_ago = (pd.Period(MONTH) - 12).strftime("%Y-%m")
growth = (m.loc[MONTH] / m.loc[year_ago] - 1) * 100
typical, spread = growth.median(), growth.std()
z = (growth - typical) / spread
stats = {"category": CATEGORY, "period": pd.Period(MONTH).strftime("%B %Y"),
         "comparison": f"same month a year earlier ({pd.Period(year_ago).strftime('%B %Y')})",
         "total_revenue_zmw": round(float(m.loc[MONTH].sum()), 2),
         "total_growth_pct": round(float((m.loc[MONTH].sum() / m.loc[year_ago].sum() - 1) * 100), 1),
         "typical_province_growth_pct": round(float(typical), 1),
         "outliers": [{"province": p, "growth_pct": round(float(growth[p]), 1), "z_score": round(float(z[p]), 2)}
                      for p in z[z.abs() >= 1.5].index]}
print(json.dumps(stats, indent=2))

prompt = ("Write three sentences for the category manager about the data below. Quote numbers exactly; "
          "do not guess causes; name what to check.\n\nData (JSON):\n" + json.dumps(stats))
client = get_client()
if client.provider.name == "mock":                     # the mock's narrative expects the chapter's keys
    stats_for_mock = {"period": stats["period"], "total_revenue_zmw": stats["total_revenue_zmw"],
                      "comparison": "January 2024", "baseline": "January 2024",
                      "change_vs_previous_pct": stats["total_growth_pct"],
                      "anomalies": [{"province": o["province"], "revenue_zmw": float(m.loc[MONTH, o["province"]]),
                                     "change_vs_typical_pct": o["growth_pct"], "z_score": o["z_score"]}
                                    for o in stats["outliers"]]}
    prompt = prompt.split("Data (JSON):")[0] + "Data (JSON):\n" + json.dumps(stats_for_mock)
reply = client.complete(prompt, system="You write short, factual notes for retail managers.")
print("\n" + reply.text)

allowed = {round(abs(v), 1) for v in pd.json_normalize(stats).select_dtypes("number").iloc[0]}
allowed |= {round(abs(o[k]), 1) for o in stats["outliers"] for k in ("growth_pct", "z_score")}
allowed |= {round(float(m.loc[MONTH, o["province"]])) for o in stats["outliers"]}
found = [float(n.replace(",", "")) for n in re.findall(r"\d[\d,]*\.?\d*", reply.text)]
unsupported = [n for n in found if n not in (2024, 2025) and not any(abs(n - a) <= 0.6 for a in allowed)]
print("\nUnsupported numbers:", unsupported or "none")
