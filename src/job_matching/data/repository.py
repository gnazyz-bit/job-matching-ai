
"""Чтение и сохранение данных вакансий."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class VacancyRepository:
    """Репозиторий вакансий, хранящихся в CSV."""

    def __init__(self, data_path: Path) -> None:
        self.data_path = Path(data_path)

    def load(self) -> pd.DataFrame:
        """Прочитать вакансии из CSV."""
        logger.info("Загрузка вакансий из %s", self.data_path)

        if not self.data_path.is_file():
            raise FileNotFoundError(
                f"Файл вакансий не найден: {self.data_path}"
            )

        try:
            vacancies = pd.read_csv(self.data_path)
        except (pd.errors.ParserError, UnicodeError) as error:
            logger.exception("Ошибка чтения CSV: %s", self.data_path)
            raise ValueError(
                f"Не удалось прочитать CSV: {self.data_path}"
            ) from error

        if vacancies.empty:
            raise ValueError("Файл вакансий пуст.")

        if "title" not in vacancies.columns:
            raise ValueError(
                "В CSV отсутствует обязательный столбец title."
            )

        logger.info("Загружено вакансий: %d", len(vacancies))
        return vacancies

    def save(self, vacancies: pd.DataFrame) -> None:
        """Безопасно сохранить вакансии в CSV."""
        if not isinstance(vacancies, pd.DataFrame):
            raise TypeError("Ожидается pandas DataFrame.")

        if vacancies.empty:
            raise ValueError("Нельзя сохранить пустой список вакансий.")

        if "title" not in vacancies.columns:
            raise ValueError(
                "В данных отсутствует обязательный столбец title."
            )

        logger.info(
            "Сохранение %d вакансий в %s",
            len(vacancies),
            self.data_path,
        )

        self.data_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path = self.data_path.with_suffix(".csv.tmp")

        try:
            vacancies.to_csv(
                temporary_path,
                index=False,
                encoding="utf-8-sig",
            )
            temporary_path.replace(self.data_path)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()

        logger.info("Вакансии успешно сохранены")
