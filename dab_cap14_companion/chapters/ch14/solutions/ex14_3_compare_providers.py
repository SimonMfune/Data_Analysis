"""Exercise 14.3 solution: the same prompt to every available provider, scored against a rubric.

Prices are not built in, because they change: enter the current price per million tokens for each
provider and model you use in PRICES (US$ input, US$ output)."""
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from shared.llm_client import KEY_VARIABLE, LLMError, get_client  # noqa: E402

MODELS = {"openai": os.getenv("OPENAI_MODEL"), "anthropic": os.getenv("ANTHROPIC_MODEL"),
          "google": os.getenv("GOOGLE_MODEL")}
PRICES = {"mock": (0.0, 0.0)}             # e.g. "openai": (1.00, 5.00) from the provider's price page

stats = {"period": "January 2025", "total_revenue_zmw": 1812201.57, "change_vs_previous_pct": -39.0,
         "anomalies": [{"province": "Copperbelt", "revenue_zmw": 377318.01, "change_vs_typical_pct": -51.0,
                        "z_score": -2.93},
                       {"province": "Central", "revenue_zmw": 156270.11, "change_vs_typical_pct": -48.8,
                        "z_score": -2.91},
                       {"province": "Lusaka", "revenue_zmw": 629826.15, "change_vs_typical_pct": -44.3,
                        "z_score": -2.55}]}
prompt = ("Write a three-sentence note for managers about unusual provincial revenue. Quote numbers exactly; "
          "do not guess causes; say what to check.\n\nData (JSON):\n" + json.dumps(stats))
allowed = {round(abs(v), 1) for a in stats["anomalies"] for v in a.values() if isinstance(v, float)}
allowed |= {round(stats["total_revenue_zmw"]), 39.0} | {round(a["revenue_zmw"]) for a in stats["anomalies"]}


def score(text):
    """Rubric: 4 points for accuracy, 2 for coverage, 2 for restraint, 2 for length."""
    nums = [float(n.replace(",", "")) for n in re.findall(r"\d[\d,]*\.?\d*", text)]
    bad = [n for n in nums if n not in (2025,) and not any(abs(n - a) <= 0.6 for a in allowed)]
    covered = sum(a["province"] in text for a in stats["anomalies"])
    guesses = len(re.findall(r"\b(because|due to|caused by|likely|probably)\b", text, re.I))
    sentences = len(re.findall(r"[.!?](\s|$)", text))
    return {"unsupported_numbers": len(bad), "accuracy": 4 if not bad else max(0, 4 - 2 * len(bad)),
            "coverage": round(2 * covered / len(stats["anomalies"]), 1), "restraint": 2 if guesses == 0 else 0,
            "length": 2 if sentences <= 4 else 1}


rows = []
for provider in ["mock"] + list(KEY_VARIABLE):
    try:
        client = get_client(provider, MODELS.get(provider))
    except LLMError as error:
        print(f"{provider:<10} skipped: {error}")
        continue
    reply = client.complete(prompt, system="You write short, factual notes for managers.")
    s = score(reply.text)
    p_in, p_out = PRICES.get(provider, (float("nan"), float("nan")))
    rows.append({"provider": provider, "model": reply.model, "seconds": reply.seconds,
                 "tokens_in": reply.input_tokens, "tokens_out": reply.output_tokens,
                 "cost_usd": reply.input_tokens / 1e6 * p_in + reply.output_tokens / 1e6 * p_out,
                 **s, "total_10": s["accuracy"] + s["coverage"] + s["restraint"] + s["length"]})
print("\n" + pd.DataFrame(rows).to_string(index=False))
