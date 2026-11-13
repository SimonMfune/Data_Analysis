"""Guards Chapter 12's printed numbers. Run from the repository root: python -m pytest chapters/ch12/tests"""
from pathlib import Path

OUT = Path("chapters/ch12/outputs")


def read(name):
    return (OUT / name).read_text()


def test_confusion_matrix_and_metrics():
    text = read("12_04_confusion.txt")
    assert "TN 478   FP 25" in text and "FN 91   TP 38" in text
    assert "Recall    TP/(TP+FN)    = 0.295" in text


def test_auc():
    assert "ROC AUC 0.775" in read("12_07_roc_pr.txt")


def test_balanced_weights_raise_recall():
    assert "recall 0.643" in read("12_06_imbalance.txt")


def test_threshold_chosen_on_training_data():
    assert "Chosen on training data: threshold 0.43" in read("12_11_costs.txt")
