
"""Тесты чтения и сохранения вакансий."""

import pandas as pd
import pytest

from job_matching.data.repository import VacancyRepository


def test_repository_load(tmp_path):
    """Репозиторий правильно загружает CSV."""
    path = tmp_path / "vacancies.csv"

    original = pd.DataFrame(
        {
            "id": [1, 2],
            "title": ["Повар", "Аналитик данных"],
        }
    )
    original.to_csv(path, index=False, encoding="utf-8-sig")

    result = VacancyRepository(path).load()

    assert len(result) == 2
    assert result["title"].tolist() == [
        "Повар",
        "Аналитик данных",
    ]


def test_repository_save(tmp_path):
    """Репозиторий сохраняет данные без изменения содержания."""
    path = tmp_path / "vacancies.csv"

    vacancies = pd.DataFrame(
        {
            "id": [1, 2],
            "title": ["Повар", "Бухгалтер"],
        }
    )

    repository = VacancyRepository(path)
    repository.save(vacancies)

    result = repository.load()

    pd.testing.assert_frame_equal(result, vacancies)


def test_repository_missing_file(tmp_path):
    """Отсутствующий CSV вызывает FileNotFoundError."""
    path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        VacancyRepository(path).load()


def test_repository_empty_csv(tmp_path):
    """CSV без вакансий отклоняется."""
    path = tmp_path / "empty.csv"

    pd.DataFrame(columns=["title"]).to_csv(
        path, index=False
    )

    with pytest.raises(ValueError, match="пуст"):
        VacancyRepository(path).load()


def test_repository_missing_title(tmp_path):
    """CSV без столбца title отклоняется."""
    path = tmp_path / "vacancies.csv"

    pd.DataFrame({"company": ["Компания"]}).to_csv(
        path, index=False
    )

    with pytest.raises(ValueError, match="title"):
        VacancyRepository(path).load()


def test_repository_rejects_empty_save(tmp_path):
    """Нельзя сохранить пустой DataFrame."""
    path = tmp_path / "vacancies.csv"

    with pytest.raises(ValueError, match="пуст"):
        VacancyRepository(path).save(
            pd.DataFrame(columns=["title"])
        )

    assert not path.exists()
