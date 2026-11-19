
"""Модели данных вакансий и резюме."""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class Resume(BaseModel):
    """Данные кандидата для сопоставления с вакансиями."""

    target_position: str = Field(min_length=1)
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[float] = Field(default=None, ge=0)
    education: Optional[str] = None
    expected_salary: Optional[float] = Field(default=None, ge=0)
    salary_currency: Optional[str] = None

    @field_validator("target_position")
    @classmethod
    def validate_position(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Укажите желаемую должность.")
        return value


class Vacancy(BaseModel):
    """Унифицированная модель вакансии."""

    id: str
    title: str = Field(min_length=1)
    description: str = ""
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[float] = Field(default=None, ge=0)
    education: Optional[str] = None
    salary_from: Optional[float] = Field(default=None, ge=0)
    salary_to: Optional[float] = Field(default=None, ge=0)
    salary_currency: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Название вакансии не может быть пустым.")
        return value

    @model_validator(mode="after")
    def validate_salary_range(self):
        if (
            self.salary_from is not None
            and self.salary_to is not None
            and self.salary_from > self.salary_to
        ):
            raise ValueError(
                "Минимальная зарплата не может превышать максимальную."
            )
        return self
