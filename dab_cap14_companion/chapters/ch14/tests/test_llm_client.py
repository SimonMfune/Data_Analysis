"""Tests for shared/llm_client.py, with no network access: each live adapter is checked against a fake
SDK client shaped like the real one. Run from the repository root: python -m pytest chapters/ch14/tests"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, str(Path.cwd()))
from shared import llm_client as lc  # noqa: E402


def test_mock_is_default_and_deterministic(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    a, b = lc.get_client(), lc.get_client()
    assert a.provider.name == "mock"
    assert a.complete("hello").text == b.complete("hello").text


def test_missing_key_and_model_give_clear_errors(monkeypatch):
    monkeypatch.setattr(lc, "ROOT", Path("/nonexistent"))      # ignore any real .env
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(lc.LLMError, match="ANTHROPIC_API_KEY is not set"):
        lc.get_client("anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    with pytest.raises(lc.LLMError, match="LLM_MODEL is not set"):
        lc.get_client("anthropic")
    with pytest.raises(lc.LLMError, match="Unknown LLM_PROVIDER"):
        lc.get_client("chatbot")


def test_openai_adapter():
    p = lc.OpenAIProvider.__new__(lc.OpenAIProvider)
    seen = {}
    def create(**kw):
        seen.update(kw)
        return NS(output_text="hi", usage=NS(input_tokens=5, output_tokens=1))
    p.client = NS(responses=NS(create=create))
    assert p.generate("q", "sys", "m", 50) == ("hi", 5, 1)
    assert seen == {"model": "m", "instructions": "sys", "input": "q", "max_output_tokens": 50}


def test_anthropic_adapter_sends_no_temperature():
    p = lc.AnthropicProvider.__new__(lc.AnthropicProvider)
    seen = {}
    def create(**kw):
        seen.update(kw)
        return NS(content=[NS(type="text", text="hi")], usage=NS(input_tokens=4, output_tokens=2))
    p.client = NS(messages=NS(create=create))
    assert p.generate("q", "sys", "m", 50) == ("hi", 4, 2)
    assert "temperature" not in seen and seen["system"] == "sys"


def test_google_adapter():
    pytest.importorskip("google.genai")
    p = lc.GoogleProvider.__new__(lc.GoogleProvider)
    seen = {}
    def generate_content(**kw):
        seen.update(kw)
        return NS(text="hi", usage_metadata=NS(prompt_token_count=3, candidates_token_count=1))
    p.client = NS(models=NS(generate_content=generate_content))
    assert p.generate("q", "sys", "m", 50) == ("hi", 3, 1)
    assert seen["config"].system_instruction == "sys"


def test_retry_on_rate_limit_then_success(monkeypatch):
    monkeypatch.setattr(lc.time, "sleep", lambda s: None)
    calls = []
    class Flaky:
        name = "flaky"
        def generate(self, *a):
            calls.append(1)
            if len(calls) < 3:
                raise type("RateLimit", (Exception,), {"status_code": 429})()
            return "ok", 1, 1
    reply = lc.LLMClient(Flaky(), "m").complete("q")
    assert reply.text == "ok" and len(calls) == 3


def test_cache_returns_identical_reply(tmp_path):
    c = lc.LLMClient(lc.MockProvider(), "mock-1", cache_dir=tmp_path)
    first = c.complete("Data (JSON):\n" + json.dumps(
        {"period": "x", "total_revenue_zmw": 1, "change_vs_previous_pct": 0, "anomalies": []}))
    second = c.complete("Data (JSON):\n" + json.dumps(
        {"period": "x", "total_revenue_zmw": 1, "change_vs_previous_pct": 0, "anomalies": []}))
    assert second.cached and second.text == first.text and c.calls == 1


def test_chapter_outputs():
    out = Path("chapters/ch14/outputs")
    assert "Unsupported numbers (careless mock): [26.0, 23.8, 19.3]" in (out / "14_07_cross_check.txt").read_text()
    assert "Labelled 1,000 of 1,000 reviews" in (out / "14_10_all_reviews.txt").read_text()
