"""Milestone M1: train, evaluate and save the pricing model. Run from this folder: python train.py"""
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict, train_test_split

from features import FEATURES, TARGET, build_model

HERE = Path(__file__).parent
DATA = HERE.parents[2] / "data" / "clean" / "kb_product_pricing.csv"
SEED, COVERAGE = 2026, 0.80


def main():
    # TODO M1: write this function
    raise NotImplementedError("M1: main")


if __name__ == "__main__":
    main()
