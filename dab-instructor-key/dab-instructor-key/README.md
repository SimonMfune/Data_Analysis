# Instructor answer key — Kwacha Basket data (do not distribute to students)

- `answer_key.json` — every defect planted in the Chapter 3 and Chapter 6 files (counts, affected order IDs),
  the Chapter 10 A/B and fraud-flag figures, and the Chapter 12 churn rate.
- `payments_fraud_truth.csv` — the hidden true fraud label for every payment (Chapter 10, Bayes' theorem).
- `customer_latent_traits.csv` — the simulated loyalty, remoteness and lifetime behind each customer's behaviour.

Regenerate together with the student data:
`python data/generator/generate_data.py --instructor <folder>`
