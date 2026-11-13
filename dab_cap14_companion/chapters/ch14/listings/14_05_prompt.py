def narrative_prompt(stats: dict) -> tuple[str, str]:
    """Role, context, data and output instructions, kept separate and in a fixed order."""
    system = ("You are an analyst at Kwacha Basket, an online retailer in Zambia. You write short, "
              "factual notes for managers. Use only the numbers in the data provided.")
    prompt = (
        "Context: the monthly sales review needs a three-sentence note on unusual provincial revenue.\n"
        "Rules: quote numbers exactly as given (amounts in kwacha with a K prefix); do not guess causes; "
        "say what should be checked; if there are no anomalies, say so.\n\n"
        f"Data (JSON):\n{json.dumps(stats)}\n\n"
        "Write the note now, in plain English, with no headings.")
    return system, prompt

system, prompt = narrative_prompt(stats)
print(system)
print("---")
print(prompt)
