"""The three business rules agreed with the pricing manager in Chapter 11.
Rule 3, showing the typical error beside every suggestion, is applied in the app."""
import math

MIN_MARKUP = 1.10                 # rule 1: never suggest less than cost + 10%
ENDINGS = (0.00, 0.50, 0.99)      # rule 2: the company's price endings


def round_to_ending(price: float, minimum: float = 0.0) -> float:
    """The price ending in .00, .50 or .99 that is nearest to `price` and not below `minimum`."""
    # TODO M2: write this function
    raise NotImplementedError("M2: round_to_ending")


def apply_guardrails(model_price: float, unit_cost: float) -> tuple[float, list[str]]:
    """Return the price to suggest and notes explaining any rule that changed it materially."""
    # TODO M2: write this function
    raise NotImplementedError("M2: apply_guardrails")
