"""Exercise 10.2 solution: a Bayes calculator for the fraud flag."""
import numpy as np
import pandas as pd


def p_fraud_given_flag(base_rate: float, sensitivity: float = 0.90, false_alarm: float = 0.03) -> float:
    """P(fraud | flag) by Bayes' theorem."""
    flagged_fraud = sensitivity * base_rate
    flagged_genuine = false_alarm * (1 - base_rate)
    return flagged_fraud / (flagged_fraud + flagged_genuine)


def break_even_base_rate(sensitivity: float = 0.90, false_alarm: float = 0.03) -> float:
    """The base rate at which a flagged payment is equally likely to be fraud or genuine."""
    return false_alarm / (sensitivity + false_alarm)


if __name__ == "__main__":
    rates = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10]
    table = pd.DataFrame({"base_rate": rates,
                          "P(fraud | flag)": [p_fraud_given_flag(r) for r in rates],
                          "with 1% false alarms": [p_fraud_given_flag(r, false_alarm=0.01) for r in rates]})
    print(table.to_string(index=False, formatters={c: "{:.1%}".format for c in table.columns}))
    print(f"\nBreak-even base rate: {break_even_base_rate():.2%}")
    assert np.isclose(p_fraud_given_flag(break_even_base_rate()), 0.5)
