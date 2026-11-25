
"""Расчёт текстового сходства резюме и вакансий."""

from collections.abc import Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_title_similarity(
    target_position: str,
    vacancy_titles: Sequence[str],
) -> np.ndarray:
    """Рассчитать сходство названия должности с названиями вакансий.

    Args:
        target_position: Нормализованная желаемая должность.
        vacancy_titles: Последовательность названий вакансий.

    Returns:
        Массив оценок косинусного сходства от 0 до 1.

    Raises:
        ValueError: При отсутствии корректных текстов.
        TypeError: При некорректных типах входных данных.
    """
    if not isinstance(target_position, str):
        raise TypeError("Должность должна быть строкой.")

    if not target_position.strip():
        raise ValueError("Должность не может быть пустой.")

    if isinstance(vacancy_titles, (str, bytes)):
        raise TypeError("Ожидается последовательность названий вакансий.")

    titles = list(vacancy_titles)

    if not titles:
        raise ValueError("Список вакансий пуст.")

    if any(not isinstance(title, str) for title in titles):
        raise TypeError("Все названия вакансий должны быть строками.")

    texts = [target_position] + titles

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
    )

    try:
        matrix = vectorizer.fit_transform(texts)
    except ValueError as error:
        raise ValueError(
            "Не удалось построить TF-IDF: проверьте тексты вакансий."
        ) from error

    similarities: np.ndarray = cosine_similarity(
        matrix[0:1],
        matrix[1:],
    ).flatten()

    return similarities
