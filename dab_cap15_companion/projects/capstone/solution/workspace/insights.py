"""Page 5: AI recommendations grounded in model output, with three guardrails (Chapter 14):
grounding (only computed figures are sent), validation (every number and feature is checked),
and disclosure (the page and the report label the text as AI-generated)."""
import json
import re
from typing import Literal

import pandas as pd
from pydantic import BaseModel, Field, ValidationError

from .modelling import ModelResult


class Recommendation(BaseModel):
    title: str = Field(max_length=80)
    detail: str = Field(max_length=400)
    evidence: list[float] = Field(min_length=1)          # the numbers from the data that support it
    features: list[str]                                  # the model features it relies on


class InsightReply(BaseModel):
    recommendations: list[Recommendation] = Field(min_length=1, max_length=5)
    caveats: list[str] = Field(min_length=1)
    confidence: Literal["low", "medium", "high"]


def segments(df: pd.DataFrame, result: ModelResult) -> list[dict]:
    """Target rate (or mean) by quartile of the most influential numeric feature."""
    numeric = [f for f in result.features if pd.api.types.is_numeric_dtype(df[f])]
    order = [f for f in result.coefficients["feature"] if f in numeric]
    if not order:
        return []
    feature = order[0]
    y = df[result.target]
    if result.kind == "logistic":
        y = (y == result.positive_class).astype(int)
    bands = pd.qcut(df[feature].rank(method="first"), 4, labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"])
    out = []
    for band, g in y.groupby(bands, observed=True):
        lo, hi = df.loc[g.index, feature].min(), df.loc[g.index, feature].max()
        out.append({"feature": feature, "quartile": str(band), "range": f"{lo:g} to {hi:g}",
                    "rows": int(len(g)), "target_mean": round(float(g.mean()), 3)})
    return out


def payload(df: pd.DataFrame, result: ModelResult) -> dict:
    """Everything the model may use: computed figures only, rounded, with no rows of data."""
    effects = result.coefficients.head(6)
    numeric = {f for f in result.features if pd.api.types.is_numeric_dtype(df[f])}
    top = [{"feature": r.feature, "type": "number" if r.feature in numeric else "category level",
            "coefficient": round(float(r.coefficient), 3),
            **({"odds_ratio": round(float(r.odds_ratio), 3)} if result.kind == "logistic" else {})}
           for r in effects.itertuples()]
    return {"insight_request": "recommendations",
            "target": result.target, "model": f"{result.kind} regression",
            "positive_class": None if result.positive_class is None else str(result.positive_class),
            "effects": "numbers: per one standard deviation; category levels: compared with the reference level",
            "rows_train": result.n_train, "rows_test": result.n_test,
            "metrics": {k: round(v, 3) for k, v in result.metrics.items()},
            "top_effects": top, "segments": segments(df, result)}


def prompt(data: dict, audience: str) -> tuple[str, str]:
    system = ("You are a senior analyst at Kwacha Basket, an online retailer in Zambia. You turn model "
              "results into practical recommendations. You use only figures in the data provided.")
    user = (f"Context: {audience} needs up to three recommendations based on a model of "
            f"'{data['target']}'.\n"
            "Rules: every recommendation must cite, in 'evidence', the exact numbers from the data that "
            "support it, and list in 'features' the model features it relies on. Effects are associations, "
            "not proof of cause: say so in 'caveats'. Set 'confidence' from the test metrics. Do not invent "
            "figures, causes or features.\n\n"
            f"Data (JSON):\n{json.dumps(data)}\n\n"
            'Return only JSON with keys "recommendations" (list of objects with title, detail, evidence, '
            'features), "caveats" (list of strings) and "confidence" (low, medium or high).')
    return system, user


def _allowed_numbers(data: dict) -> set[float]:
    found = set()
    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, (int, float)) and not isinstance(x, bool):
            found.add(round(abs(float(x)), 3))
        elif isinstance(x, str):
            for n in re.findall(r"\d+\.?\d*", x):
                found.add(round(float(n), 3))
    walk(data)
    return found


def validate(reply_text: str, data: dict) -> tuple[InsightReply | None, list[str]]:
    """Parse the reply against the schema, then check every number and feature against the data."""
    try:
        reply = InsightReply.model_validate_json(reply_text.strip().removeprefix("```json").removesuffix("```"))
    except ValidationError as error:
        return None, [f"The reply does not match the required format: {str(error).splitlines()[0]}"]
    allowed = _allowed_numbers(data)
    features = {e["feature"] for e in data["top_effects"]} | {s["feature"] for s in data["segments"]}

    def supported(n):
        return any(abs(abs(n) - a) <= max(0.0051, 0.005 * a) for a in allowed) or \
               any(abs(abs(n) - a * 100) <= 0.051 for a in allowed if a <= 1)      # 0.213 quoted as 21.3%

    problems = []
    for i, rec in enumerate(reply.recommendations, 1):
        for n in rec.evidence:
            if not supported(n):
                problems.append(f"Recommendation {i}: evidence {n:g} is not in the model output")
        for n in [float(x) for x in re.findall(r"\d+\.?\d*", rec.detail)]:
            if not supported(n):
                problems.append(f"Recommendation {i}: the figure {n:g} in the text is not in the model output")
        for f in rec.features:
            if f not in features:
                problems.append(f"Recommendation {i}: feature {f!r} was not among the model's top effects")
    return reply, problems
