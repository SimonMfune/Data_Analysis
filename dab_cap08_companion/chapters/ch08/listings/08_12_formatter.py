from matplotlib.ticker import FuncFormatter

def kwacha(value, position=None):
    """Format a number of kwacha for an axis: K950, K12k, K1.5m."""
    if abs(value) >= 1_000_000:
        return f"K{value / 1_000_000:.1f}m"
    if abs(value) >= 1_000:
        return f"K{value / 1_000:.0f}k"
    return f"K{value:.0f}"

print([kwacha(v) for v in [950, 12_400, 1_500_000, 4_581_517]])
