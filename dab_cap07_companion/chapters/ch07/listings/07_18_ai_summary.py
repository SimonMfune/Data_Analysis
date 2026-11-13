summary = {
    "customers": len(customers),
    "spend_median_zmw": round(spend.median()),
    "spend_by_age_band_median": by_age["median_spend"].round(0).to_dict(),
    "late_pct_by_province": late["late_pct"].round(1).to_dict(),
    "orders_per_day_by_weekday": counts.div(len(calendar) / 7).round(1).to_dict(),
}
import textwrap
for key, value in summary.items():
    print(textwrap.fill(f"{key}: {value}", width=80, subsequent_indent="    "))
