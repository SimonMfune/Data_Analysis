"""The three business rules agreed with the pricing manager in Chapter 11.
Rule 3, showing the typical error beside every suggestion, is applied in the app."""
import math

MIN_MARKUP = 1.10                 # rule 1: never suggest less than cost + 10%
ENDINGS = (0.00, 0.50, 0.99)      # rule 2: the company's price endings


def round_to_ending(price: float, minimum: float = 0.0) -> float:
    """The price ending in .00, .50 or .99 that is nearest to `price` and not below `minimum`."""
    base = math.floor(price)
    candidates = [b + e for b in (base - 1, base, base + 1) for e in ENDINGS if b + e >= minimum]
    return round(min(candidates, key=lambda c: (abs(c - price), c)), 2)


def apply_guardrails(model_price: float, unit_cost: float) -> tuple[float, list[str]]:
    """Return the price to suggest and notes explaining any rule that changed it materially."""
    notes = []
    floor = unit_cost * MIN_MARKUP
    price = model_price
    if price < floor:
        price = floor
        notes.append(f"Raised to cost + 10% (K{floor:,.2f}); the model suggested K{model_price:,.2f}")
    return round_to_ending(price, minimum=floor), notes
