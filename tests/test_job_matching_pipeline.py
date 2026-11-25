from __future__ import annotations

import pandas as pd

from job_matching.ml.features import experience_fit, salary_fit
from job_matching.ml.training import make_weak_labels
from job_matching.services.cover_letter_service import create_cover_letter
from job_matching.services.recommendation_service import resume_advice


def test_experience_seniority():
    assert experience_fit(0, "['Senior']") == 0.0
    assert experience_fit(0, "['Entry-level']") == 1.0


def test_salary_mismatched_currencies_is_unknown():
    value, known = salary_fit(1000, "USD", {"salary_to": 400000, "salary_currency": "KZT", "salary_period": "monthly"})
    assert (value, known) == (0.5, 0.0)


def test_synthetic_labels_are_binary():
    rows = pd.DataFrame({"role_overlap": [1.0, 0.0], "title_similarity": [0.6, 0.0],
                         "skill_overlap": [0.5, 0.0], "experience_fit": [1.0, 0.0]})
    assert make_weak_labels(rows).tolist() == [1, 0]


def test_letter_does_not_invent_experience():
    letter = create_cover_letter({"name": "Test", "skills": ["SQL"]}, {"title": "Data Analyst", "company": "Example"}, "SQL")
    assert "SQL" in letter and "5 years" not in letter


def test_resume_advice_does_not_assert_missing_skill():
    notes = resume_advice({"mentioned_skills": "SQL, Python"}, {"skills": ["SQL"]})
    assert "only if true" in notes[0] and "Python" in notes[0]
