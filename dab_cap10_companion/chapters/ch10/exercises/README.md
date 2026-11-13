# Chapter 10 exercises

Run from the repository root, e.g. `python chapters/ch10/solutions/ex10_1_late_simulation.py`.

- **10.1 (Core)** Using the late rate for each province in `data/clean/kb_delivery_times.csv`, simulate
  10,000 weeks in which a courier makes 20 deliveries in that province. Chart the distribution of late
  deliveries per week for Lusaka, Copperbelt, Northern and Western, and report for each province the
  probability that 5 or more of the 20 are late. Check one province against `scipy.stats.binom`.
- **10.2 (Stretch)** Write `p_fraud_given_flag(base_rate, sensitivity, false_alarm)` and use it to build a
  table of P(fraud | flag) for base rates from 0.1% to 10%. Then make it a small Streamlit app with three
  sliders. At what base rate is a flagged payment more likely fraud than not?
- **10.3 (Challenge)** Analyse the WhatsApp-versus-SMS test in `data/clean/kb_campaign_ab.csv` in full:
  state the hypotheses, test clicks and conversions, compute effect sizes and 95% confidence intervals, estimate
  revenue per contact with a bootstrap interval, check whether the result holds for existing and new
  customers, and write a recommendation of no more than 150 words.
