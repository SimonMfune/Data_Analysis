margin_at_risk = churn.loc[churn["churned"] == 1, "spend_last_180d_zmw"].mean() * 0.365
voucher, save_rate = 150, 0.30           # a K150 voucher keeps 30% of real churners
gain_tp = save_rate * margin_at_risk - voucher
print(f"Gross margin a churner would bring in the next six months: about K{margin_at_risk:,.0f}")
print(f"Flagging a real churner is worth 0.30 x K{margin_at_risk:,.0f} - K{voucher} = K{gain_tp:,.0f}; "
      f"flagging a stayer costs K{voucher}")

def net_benefit(y_true, p, threshold):
    flag = p >= threshold
    tp = (flag & (y_true == 1)).sum()
    fp = (flag & (y_true == 0)).sum()
    return tp * gain_tp - fp * voucher

# Choose the threshold on the training data (out-of-fold predictions), not on the test set
oof_train = cross_val_predict(model, X_train, y_train, cv=folds, method="predict_proba")[:, 1]
thresholds = np.round(np.arange(0.05, 0.81, 0.01), 2)
per_1000 = np.array([net_benefit(y_train.to_numpy(), oof_train, t) for t in thresholds]) / len(y_train) * 1000
best = thresholds[per_1000.argmax()]
print(f"\nChosen on training data: threshold {best:.2f} (K{per_1000.max():,.0f} per 1,000 customers)")

for t in [best, 0.5, 0.0]:
    label = {best: "chosen threshold", 0.5: "default 0.50", 0.0: "voucher for everyone"}[t]
    print(f"Test set, {label:<21}: net benefit K{net_benefit(y_test.to_numpy(), proba, t):>8,.0f} "
          f"for {len(y_test)} customers")

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(thresholds, per_1000 / 1000)
ax.axvline(best, color="#C8553D", linewidth=1.2, linestyle="--")
ax.axvline(0.5, color="#9AA5B1", linewidth=1, linestyle=":")
ax.axhline(0, color="#1B2A41", linewidth=0.8)
low = per_1000.min() / 1000 * 0.4
ax.text(best - 0.01, low, f"chosen\n{best:.2f}", color="#C8553D", fontsize=9, ha="right")
ax.text(0.51, low, "default\n0.50", color="#4A5561", fontsize=9)
ax.set_xlabel("Decision threshold (send a voucher if P(churn) is at least this)")
ax.set_ylabel("Net benefit per 1,000 customers (K thousand)")
ax.set_title("Net benefit peaks between about 0.35 and 0.5, and turns into a loss below 0.2")
fig.savefig(FIG + "fig_12_4_net_benefit.png", dpi=200)
plt.close(fig)
