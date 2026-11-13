"""Exercise 2.2 (Stretch) — model answer.

Prints a version table and flags any package older than the minimum
version the book requires (read from requirements.txt).
Run from the repository root:  python chapters/ch02/solutions/check_env_extended.py [requirements_file]
With no argument it reads the repository's requirements.txt; pass a modified copy to test it.
"""
import re
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from packaging.version import Version

ROOT = Path(__file__).resolve().parents[3]
minimums = {}
req_file = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "requirements.txt"
for line in req_file.read_text().splitlines():
    m = re.match(r"^([A-Za-z0-9_.-]+)\s*(>=\s*([\d.]+))?", line.strip())
    if m and not line.startswith("#"):
        minimums[m.group(1)] = m.group(3)

print(f"{'Package':<15}{'Installed':<12}{'Minimum':<10}Status")
print("-" * 45)
problems = 0
for pkg, minimum in minimums.items():
    try:
        installed = version(pkg)
    except PackageNotFoundError:
        print(f"{pkg:<15}{'—':<12}{minimum or 'any':<10}MISSING")
        problems += 1
        continue
    too_old = minimum is not None and Version(installed) < Version(minimum)
    status = "TOO OLD" if too_old else "OK"
    problems += too_old
    print(f"{pkg:<15}{installed:<12}{minimum or 'any':<10}{status}")

print("-" * 45)
print("All requirements met." if not problems else f"{problems} problem(s) found.")
sys.exit(1 if problems else 0)
