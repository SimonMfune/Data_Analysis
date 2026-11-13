pred = (proba >= 0.5).astype(int)
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print(f"TN {tn}   FP {fp}\nFN {fn}   TP {tp}")
print(f"\nAccuracy  (TP+TN)/all   = {(tp + tn) / (tp + tn + fp + fn):.3f}")
print(f"Precision TP/(TP+FP)    = {tp / (tp + fp):.3f}")
print(f"Recall    TP/(TP+FN)    = {tp / (tp + fn):.3f}")
print(f"F1        harmonic mean = {2 * tp / (2 * tp + fp + fn):.3f}")
print(f"scikit-learn agrees: precision {precision_score(y_test, pred):.3f}, "
      f"recall {recall_score(y_test, pred):.3f}, F1 {f1_score(y_test, pred):.3f}")

def draw_matrix(ax, cm, title):
    ax.imshow(cm, cmap="BuGn", vmin=0, vmax=cm.max() * 1.3)
    labels = [["True negative", "False positive"], ["False negative", "True positive"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{cm[i, j]}\n{labels[i][j]}", ha="center", va="center", fontsize=10)
    ax.set_xticks([0, 1], ["Predicted: stays", "Predicted: churns"])
    ax.set_yticks([0, 1], ["Actually stayed", "Actually churned"])
    ax.grid(False)
    ax.set_title(title, fontsize=11)

fig, ax = plt.subplots(figsize=(5.6, 4.2))
draw_matrix(ax, confusion_matrix(y_test, pred), "Threshold 0.5")
fig.savefig(FIG + "fig_12_2_confusion.png", dpi=200)
plt.close(fig)
