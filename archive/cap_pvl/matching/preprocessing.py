
"""Предобработка текстовых данных для сопоставления вакансий."""

JOB_TITLES: dict[str, str] = {
    "junior data analyst": "аналитик данных",
    "data analyst": "аналитик данных",
    "python developer": "разработчик python",
    "software engineer": "инженер-программист",
    "accountant": "бухгалтер",
    "teacher": "учитель",
    "cook": "повар",
    "chef": "шеф-повар",
}


def normalize_job_title(title: str) -> str:
    """Нормализовать название желаемой должности.

    Args:
        title: Исходное название должности.

    Returns:
        Нормализованное название должности.

    Raises:
        ValueError: Если название пустое.
        TypeError: Если передано не строковое значение.
    """
    if not isinstance(title, str):
        raise TypeError("Название должности должно быть строкой.")

    cleaned_title = title.strip()

    if not cleaned_title:
        raise ValueError("Название должности не может быть пустым.")

    return JOB_TITLES.get(
        cleaned_title.lower(),
        cleaned_title,
    )
