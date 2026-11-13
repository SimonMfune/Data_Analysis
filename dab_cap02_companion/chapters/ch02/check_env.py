"""Listing 2.5 — check_env.py: confirm the book's tools are installed.

Run from the repository root:  python chapters/ch02/check_env.py
"""
import importlib
import platform
import sys
from importlib.metadata import version
from pathlib import Path

# import name -> package name (as installed by pip/conda)
PACKAGES = {"pandas": "pandas", "numpy": "numpy", "matplotlib": "matplotlib",
            "scipy": "scipy", "sklearn": "scikit-learn", "openpyxl": "openpyxl",
            "joblib": "joblib", "streamlit": "streamlit", "dotenv": "python-dotenv"}

print(f"Python {platform.python_version()} ({sys.executable})")
missing = []
for name, dist in PACKAGES.items():
    try:
        importlib.import_module(name)
        print(f"  OK   {dist:<14} {version(dist)}")
    except ImportError:
        print(f"  MISSING {dist}")
        missing.append(name)

db = Path("data") / "kwacha_basket.db"
print(f"  {'OK  ' if db.exists() else 'MISSING'} Kwacha Basket database at {db}")

if missing or not db.exists():
    print("\nSomething is missing. See 'Getting the Companion Files' in the front matter.")
    sys.exit(1)
print("\nYour environment is ready.")
