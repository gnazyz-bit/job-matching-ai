
"""Тесты сервиса сопоставления вакансий."""

import pandas as pd
import pytest

from job_matching.services.matching_service import match_vacancies


def test_matching_ranks_relevant_vacancy_first():
    """Подходящая по названию вакансия должна быть первой."""
    vacancies = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "title": [
                "Повар",
                "Аналитик данных",
                "Бухгалтер",
            ],
        }
    )

    result = match_vacancies("Data Analyst", vacancies)

    assert result.iloc[0]["id"] == 2
    assert result.iloc[0]["title_similarity"] == pytest.approx(1.0)


def test_matching_preserves_original_dataframe():
    """Сервис не должен изменять исходные вакансии."""
    vacancies = pd.DataFrame(
        {"title": ["Повар", "Аналитик данных"]}
    )

    match_vacancies("Data Analyst", vacancies)

    assert "title_similarity" not in vacancies.columns


def test_matching_rejects_empty_vacancies():
    """Пустой список вакансий вызывает ошибку."""
    vacancies = pd.DataFrame(columns=["title"])

    with pytest.raises(ValueError, match="пуст"):
        match_vacancies("Data Analyst", vacancies)


def test_matching_rejects_missing_title_column():
    """Обязательный столбец title должен присутствовать."""
    vacancies = pd.DataFrame({"company": ["Компания"]})

    with pytest.raises(ValueError, match="title"):
        match_vacancies("Data Analyst", vacancies)


def test_matching_rejects_empty_position():
    """Нельзя сопоставлять вакансии с пустой должностью."""
    vacancies = pd.DataFrame({"title": ["Аналитик данных"]})

    with pytest.raises(ValueError):
        match_vacancies("", vacancies)
