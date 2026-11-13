findings = pd.DataFrame([
    {"id": "F1", "question": "Does spending cluster around month-end?",
     "evidence": "65.0 vs 49.9 orders/day (Listing 7.8)", "status": "Confirmed",
     "next_step": "Time promotions for the 25th"},
    {"id": "F2", "question": "Is December the peak month?",
     "evidence": "Dec 2025 revenue 1.99x other 2025 months (7.7)", "status": "Confirmed",
     "next_step": "Stock up from October"},
    {"id": "F3", "question": "Are repeat purchases falling?",
     "evidence": "90-day repeat 79.1% -> 86.5% (7.15)", "status": "Rejected",
     "next_step": "Look elsewhere for the revenue worry"},
    {"id": "F4", "question": "Are distant provinces served worse?",
     "evidence": "Late: Western 20.1%, Lusaka 10.8% (7.16)", "status": "Confirmed",
     "next_step": "Review courier contracts"},
    {"id": "F5", "question": "Do customers who return more spend less?",
     "evidence": "Spearman +0.39 per order (7.12)", "status": "Rejected",
     "next_step": "Check whether bigger baskets drive both"},
])
findings.to_csv("chapters/ch07/outputs/findings_log.csv", index=False)
for row in findings.itertuples():
    print(f"{row.id}  {row.status:<9}  {row.question}")
