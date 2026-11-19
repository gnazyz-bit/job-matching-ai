
"""Ранжирование вакансий по оценке текстового сходства."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd


def rank_vacancies(
    vacancies: pd.DataFrame,
    scores: Sequence[float] | np.ndarray,
) -> pd.DataFrame:
    """Отсортировать вакансии по убыванию сходства.

    При равных оценках сохраняется исходный порядок вакансий.
    Исходный DataFrame не изменяется.
    """
    if vacancies.empty:
        raise ValueError("Список вакансий пуст.")

    scores_array = np.asarray(scores, dtype=float)

    if scores_array.ndim != 1:
        raise ValueError("Оценки должны быть одномерным массивом.")

    if len(vacancies) != len(scores_array):
        raise ValueError(
            "Количество оценок должно совпадать "
            "с количеством вакансий."
        )

    if not np.all(np.isfinite(scores_array)):
        raise ValueError("Оценки должны быть конечными числами.")

    if np.any((scores_array < 0) | (scores_array > 1)):
        raise ValueError("Оценки сходства должны быть от 0 до 1.")

    result = vacancies.copy()
    result["title_similarity"] = scores_array

    return result.sort_values(
        by="title_similarity",
        ascending=False,
        kind="stable",
    )
