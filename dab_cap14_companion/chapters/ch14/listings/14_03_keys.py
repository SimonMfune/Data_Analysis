import os

from dotenv import load_dotenv

load_dotenv(".env")                        # reads KEY=value lines into the environment, if the file exists

for name in ["LLM_PROVIDER", "LLM_MODEL", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]:
    value = os.getenv(name)
    if value and name.endswith("_KEY"):
        shown = value[:4] + "..." + f" ({len(value)} characters)"   # never print a whole key
    else:
        shown = value or "(not set)"
    print(f"{name:<18} {shown}")

ignored = Path(".gitignore").read_text().splitlines()
print("\n.env is listed in .gitignore:", ".env" in ignored)
