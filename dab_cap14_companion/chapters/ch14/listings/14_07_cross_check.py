def numbers_in(text):
    """Every number in a piece of text, as floats (commas, K and % removed)."""
    return [float(n.replace(",", "")) for n in re.findall(r"[-+]?\d[\d,]*\.?\d*", text)]

def cross_check(narrative, stats, tolerance=0.06):
    """Each number in the narrative must match a number in the data (allowing rounding)."""
    allowed = set()
    for value in pd.json_normalize(stats).iloc[0].to_list() + [
            v for a in stats["anomalies"] for v in a.values() if isinstance(v, (int, float))]:
        if isinstance(value, (int, float)):
            allowed.update({round(abs(value), 1), round(abs(value)), round(abs(value), 2)})
    years = {2023.0, 2024.0, 2025.0, 2026.0, 12.0, 2.0}       # dates and the method's own numbers
    return [n for n in numbers_in(narrative)
            if abs(n) not in years and not any(abs(abs(n) - a) <= tolerance for a in allowed)]

print("Unsupported numbers (honest mock):", cross_check(reply.text, stats) or "none")

careless = get_client("mock", mistakes=True)              # a provider that misquotes one figure
bad = careless.complete(prompt, system=system)
print("\nCareless reply:", bad.text[:200], "...")
print("Unsupported numbers (careless mock):", cross_check(bad.text, stats) or "none")
