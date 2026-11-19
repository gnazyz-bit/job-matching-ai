
"""Сервис сопоставления резюме с вакансиями."""

import logging

import pandas as pd

from job_matching.matching.preprocessing import normalize_job_title
from job_matching.matching.ranking import rank_vacancies
from job_matching.matching.similarity import calculate_title_similarity

logger = logging.getLogger(__name__)


def match_vacancies(
    target_position: str,
    vacancies: pd.DataFrame,
) -> pd.DataFrame:
    """Ранжировать вакансии по сходству названий должностей."""
    if not isinstance(vacancies, pd.DataFrame):
        raise TypeError("Вакансии должны быть представлены DataFrame.")

    if vacancies.empty:
        raise ValueError("Список вакансий пуст.")

    if "title" not in vacancies.columns:
        raise ValueError("Отсутствует обязательный столбец title.")

    normalized_position = normalize_job_title(target_position)

    logger.info(
        "Начало сопоставления: должность='%s', вакансий=%d",
        normalized_position,
        len(vacancies),
    )

    titles = vacancies["title"].fillna("").astype(str).tolist()

    scores = calculate_title_similarity(
        target_position=normalized_position,
        vacancy_titles=titles,
    )

    result = rank_vacancies(vacancies, scores)

    logger.info(
        "Сопоставление завершено: обработано %d вакансий",
        len(result),
    )

    return result
