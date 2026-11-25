from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GroupShuffleSplit

from job_matching.ml.features import FEATURES


def make_weak_labels(rows):
    """Transparent synthetic examples, intentionally NOT human ground truth."""
    role = rows["role_overlap"] >= 0.5
    text = rows["title_similarity"] >= 0.27
    skills = rows["skill_overlap"] >= 0.20
    exp = rows["experience_fit"] >= 0.38
    # Role gate prevents arbitrary shared 'analyst' words from determining a match.
    return ((role & (text | skills) & exp)).astype(int)


def train_classifier(features: pd.DataFrame, profile_count: int):
    """Train on synthetic labels; hold out entire vacancy IDs to limit leakage."""
    synthetic = features.copy()
    synthetic["label"] = make_weak_labels(synthetic)
    if synthetic["label"].nunique() < 2:
        raise ValueError("Synthetic labels contain only one class")
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(splitter.split(synthetic, synthetic["label"], groups=synthetic["vacancy_id"]))
    train, test = synthetic.iloc[train_idx], synthetic.iloc[test_idx]
    if train["label"].nunique() < 2 or test["label"].nunique() < 2:
        raise ValueError("The training or evaluation split contains only one class")
    classifier = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    classifier.fit(train[FEATURES], train["label"])
    metrics = classification_report(test["label"], classifier.predict(test[FEATURES]), zero_division=0)
    return classifier, synthetic, metrics, len(train), len(test)
