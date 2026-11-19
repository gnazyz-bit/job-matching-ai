
"""Тесты моделей резюме и вакансий."""

import pytest
from pydantic import ValidationError

from job_matching.domain.models import Resume, Vacancy


def test_valid_resume():
    """Корректное резюме успешно создаётся."""
    resume = Resume(
        target_position="Data Analyst",
        skills=["Python", "SQL"],
        experience_years=2,
    )

    assert resume.target_position == "Data Analyst"
    assert resume.experience_years == 2
    assert resume.skills == ["Python", "SQL"]


def test_empty_target_position():
    """Пустая должность не допускается."""
    with pytest.raises(ValidationError):
        Resume(target_position="   ")


def test_negative_experience():
    """Опыт работы не может быть отрицательным."""
    with pytest.raises(ValidationError):
        Resume(
            target_position="Data Analyst",
            experience_years=-1,
        )


def test_valid_vacancy():
    """Корректная вакансия успешно создаётся."""
    vacancy = Vacancy(
        id="123",
        title="Python Developer",
        salary_from=1000,
        salary_to=2000,
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.salary_from == 1000


def test_invalid_salary_range():
    """Минимальная зарплата не может превышать максимальную."""
    with pytest.raises(ValidationError):
        Vacancy(
            id="123",
            title="Python Developer",
            salary_from=3000,
            salary_to=1000,
        )


def test_empty_vacancy_title():
    """Название вакансии не может быть пустым."""
    with pytest.raises(ValidationError):
        Vacancy(
            id="123",
            title="   ",
        )
