"""Guards Chapter 10's printed numbers and the Bayes calculator. Run from the repository root:
    python -m pytest chapters/ch10/tests"""
import sys
from pathlib import Path

import pytest

OUT = Path("chapters/ch10/outputs")
sys.path.insert(0, "chapters/ch10/solutions")
from ex10_2_bayes_calculator import break_even_base_rate, p_fraud_given_flag  # noqa: E402


def read(name):
    return (OUT / name).read_text()


def test_bayes_posterior():
    assert p_fraud_given_flag(0.005) == pytest.approx(0.1310, abs=1e-4)
    assert "P(fraud | flag) = 0.131" in read("10_04_bayes.txt")
    assert p_fraud_given_flag(break_even_base_rate()) == pytest.approx(0.5)


def test_flag_rate_matches_model():
    assert "1,637 of 47,460 digital payments were flagged (0.0345)" in read("10_04_bayes.txt")


def test_ab_test():
    text = read("10_14_ab_test.txt")
    assert "z = 3.33  two-sided p = 0.0009" in text
    assert "0.0065 to 0.0251" in text


def test_conditional_late():
    text = read("10_03_conditional.txt")
    assert "P(late | Lusaka)  = 0.108" in text and "P(late | Western) = 0.201" in text
