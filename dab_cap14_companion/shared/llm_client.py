"""One small, provider-neutral helper for calling large language models (Chapter 14).

    from shared.llm_client import get_client
    client = get_client()                         # reads LLM_PROVIDER and LLM_MODEL from .env
    reply = client.complete("Explain gross margin in one sentence.")
    print(reply.text, reply.input_tokens, reply.output_tokens)

Providers: "mock" (offline, free, deterministic; the default), "openai", "anthropic", "google".
Model names are never hard-coded: set LLM_MODEL to a current model from the provider's model list.

Design rules:
* Every provider returns the same LLMResponse, so analysis code never changes when the provider does.
* Sampling settings such as temperature are not sent. Several current models from all three providers
  reject or ignore them; reproducibility comes from validation and caching instead (Section 14.8).
* Responses can be cached on disk, keyed by provider, model and prompt, so reruns cost nothing.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY_VARIABLE = {"openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "google": "GOOGLE_API_KEY"}


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    seconds: float
    cached: bool = False


class LLMError(RuntimeError):
    """Raised with a plain-English message when a call cannot be completed."""


# --------------------------------------------------------------------------- providers
class OpenAIProvider:
    name = "openai"

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt, system, model, max_tokens):
        r = self.client.responses.create(model=model, instructions=system, input=prompt,
                                         max_output_tokens=max_tokens)
        return r.output_text, r.usage.input_tokens, r.usage.output_tokens


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt, system, model, max_tokens):
        kwargs = {"system": system} if system else {}
        r = self.client.messages.create(model=model, max_tokens=max_tokens,
                                        messages=[{"role": "user", "content": prompt}], **kwargs)
        text = "".join(block.text for block in r.content if block.type == "text")
        return text, r.usage.input_tokens, r.usage.output_tokens


class GoogleProvider:
    name = "google"

    def __init__(self, api_key: str):
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt, system, model, max_tokens):
        from google.genai import types
        config = types.GenerateContentConfig(system_instruction=system, max_output_tokens=max_tokens)
        r = self.client.models.generate_content(model=model, contents=prompt, config=config)
        usage = r.usage_metadata
        return r.text or "", usage.prompt_token_count or 0, usage.candidates_token_count or 0


class MockProvider:
    """An offline stand-in that answers the chapter's prompts deterministically.

    It recognises two kinds of request and otherwise replies generically:
    * a prompt containing a "Data (JSON):" block -> a short narrative that quotes the data;
    * a prompt asking for review themes as JSON -> keyword-based themes and sentiment.
    With mistakes=True it deliberately changes one number or one theme, so that the
    validation checks in Section 14.8 have something to catch.
    """
    name = "mock"
    THEMES = {
        "delivery": ["deliver", "courier", "driver", "arriv", "came earlier", "waited", "took too long",
                     "find my house", "kept me updated", "next day"],
        "price_value": ["price", "value", "cheaper", "expensive", "discount", "worth", "fee"],
        "product_quality": ["quality", "original", "picture", "well made", "broke", "damaged", "scratched"],
        "payment": ["payment", "paying", "mobile money", "charged", "unpaid", "refund", "checkout"],
        "customer_service": ["customer care", "staff", "explain my problem", "did not respond", "answered"],
        "pickup_point": ["pickup point"],
    }
    NEGATIVE = ["late", "waited", "no updates", "not the same", "too long", "could not", "charged but",
                "damaged", "did not respond", "nobody", "went up", "too expensive", "three times",
                "poor quality", "failed", "too high", "broke"]

    def __init__(self, mistakes: bool = False):
        self.mistakes = mistakes

    def generate(self, prompt, system, model, max_tokens):
        if "review_id" in prompt and "JSON" in prompt:
            text = self._themes(prompt)
        elif "Data (JSON):" in prompt:
            text = self._narrative(prompt)
        else:
            text = ("[mock reply] This is the offline practice provider. Set LLM_PROVIDER and LLM_MODEL "
                    "in .env to send this prompt to a real model.")
        return text, estimate_tokens((system or "") + prompt), estimate_tokens(text)

    def _narrative(self, prompt):
        data = json.loads(prompt.split("Data (JSON):", 1)[1].strip().split("\n\n")[0])
        lines = [f"{data['period']}: total revenue was K{data['total_revenue_zmw']:,.0f}, "
                 f"{data['change_vs_previous_pct']:+.1f}% on {data.get('comparison', 'the previous month')}."]
        for a in data["anomalies"]:
            pct = a["change_vs_typical_pct"] + (25.0 if self.mistakes else 0.0)
            direction = "above" if pct > 0 else "below"
            lines.append(f"{a['province']} stood out at K{a['revenue_zmw']:,.0f}, {abs(pct):.1f}% "
                         f"{direction} {data.get('baseline', 'its typical month')} (z = {a['z_score']:+.1f}).")
        lines.append("These are statistical flags, not explanations; check stock, campaigns and "
                     "deliveries in the flagged provinces before acting.")
        return " ".join(lines)

    def _themes(self, prompt):
        block = prompt[prompt.index("["):prompt.rindex("]") + 1]
        out = []
        for i, review in enumerate(json.loads(block)):
            text = review["text"].lower()
            themes = [t for t, words in self.THEMES.items() if any(w in text for w in words)]
            negatives = sum(w in text for w in self.NEGATIVE)
            positives = len(re.findall(r"[.!]", text)) - negatives
            sentiment = "negative" if negatives > positives else "positive" if negatives == 0 else "mixed"
            if self.mistakes and i == 0:
                themes = ["store_hygiene"]                      # a theme outside the allowed list
            out.append({"review_id": review["review_id"], "sentiment": sentiment, "themes": themes})
        return json.dumps(out)


# --------------------------------------------------------------------------- client
def estimate_tokens(text: str) -> int:
    """Rough token count: about four characters of English per token."""
    return max(1, round(len(text) / 4))


class LLMClient:
    """Calls one provider, with retries, optional disk caching and token accounting."""

    def __init__(self, provider, model: str, max_output_tokens: int = 1000,
                 cache_dir: Path | None = None, retries: int = 3):
        self.provider, self.model = provider, model
        self.max_output_tokens, self.retries = max_output_tokens, retries
        self.cache_dir = cache_dir
        self.calls = self.input_tokens = self.output_tokens = 0

    def _cache_path(self, prompt, system):
        key = json.dumps([self.provider.name, self.model, system, prompt, self.max_output_tokens])
        return self.cache_dir / f"{hashlib.sha256(key.encode()).hexdigest()[:24]}.json"

    def complete(self, prompt: str, system: str | None = None) -> LLMResponse:
        """Send one prompt and return an LLMResponse. Retries rate limits and server errors."""
        if self.cache_dir:
            path = self._cache_path(prompt, system)
            if path.exists():
                return LLMResponse(**{**json.loads(path.read_text()), "cached": True, "seconds": 0.0})
        start = time.perf_counter()
        for attempt in range(self.retries + 1):
            try:
                text, n_in, n_out = self.provider.generate(prompt, system, self.model, self.max_output_tokens)
                break
            except Exception as error:                 # each SDK has its own error classes
                status = getattr(error, "status_code", None) or getattr(error, "code", None)
                if attempt < self.retries and status in (429, 500, 502, 503, 529):
                    time.sleep(2 ** attempt)           # 1, 2, 4 seconds
                    continue
                raise LLMError(f"{self.provider.name} call failed ({error.__class__.__name__}): "
                               f"{str(error)[:200]}") from error
        reply = LLMResponse(text, self.provider.name, self.model, n_in, n_out,
                            round(time.perf_counter() - start, 3))
        self.calls += 1
        self.input_tokens += n_in
        self.output_tokens += n_out
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(asdict(reply)))
        return reply


def get_client(provider: str | None = None, model: str | None = None, *, mistakes: bool = False,
               cache: bool = False, max_output_tokens: int = 1000) -> LLMClient:
    """Build a client from arguments or from the environment (.env).

    LLM_PROVIDER: mock (default), openai, anthropic or google.
    LLM_MODEL: required for live providers, e.g. a current model name from the provider's model list.
    """
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except ImportError:
        pass
    name = (provider or os.getenv("LLM_PROVIDER") or "mock").strip().lower()
    cache_dir = ROOT / ".llm_cache" if cache else None
    if name == "mock":
        return LLMClient(MockProvider(mistakes=mistakes), model or "mock-1",
                         max_output_tokens, cache_dir)
    if name not in KEY_VARIABLE:
        raise LLMError(f"Unknown LLM_PROVIDER {name!r}. Use mock, openai, anthropic or google.")
    key = os.getenv(KEY_VARIABLE[name])
    if not key:
        raise LLMError(f"{KEY_VARIABLE[name]} is not set. Add it to .env (never to your code).")
    model = model or os.getenv("LLM_MODEL")
    if not model:
        raise LLMError("LLM_MODEL is not set. Choose a current model from the provider's model list.")
    providers = {"openai": OpenAIProvider, "anthropic": AnthropicProvider, "google": GoogleProvider}
    return LLMClient(providers[name](key), model, max_output_tokens, cache_dir)
