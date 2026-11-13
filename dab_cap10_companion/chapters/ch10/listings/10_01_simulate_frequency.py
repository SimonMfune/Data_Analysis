# A fair six-sided die: the long-run share of sixes approaches 1/6
rolls = rng.integers(1, 7, size=100_000)
for n in [10, 100, 1_000, 100_000]:
    print(f"{n:>7,} rolls: share of sixes = {(rolls[:n] == 6).mean():.4f}")
print(f"Theory: {1 / 6:.4f}")
