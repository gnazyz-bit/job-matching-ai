
"""Загрузка и валидация резюме из JSON."""

import json
import logging
from pathlib import Path

from pydantic import ValidationError

from job_matching.domain.models import Resume

logger = logging.getLogger(__name__)


class ResumeRepository:
    """Репозиторий резюме, хранящихся в JSON."""

    def load(self, path: Path) -> Resume:
        """Прочитать и проверить резюме."""
        path = Path(path)

        logger.info("Загрузка резюме из %s", path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Файл резюме не найден: {path}"
            )

        try:
            with path.open("r", encoding="utf-8-sig") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeError) as error:
            logger.exception("Ошибка чтения JSON: %s", path)
            raise ValueError("Некорректный JSON-файл резюме.") from error

        if not isinstance(data, dict):
            raise ValueError("Резюме должно быть JSON-объектом.")

        try:
            resume = Resume.model_validate(data)
        except ValidationError:
            logger.exception("Ошибка валидации резюме: %s", path)
            raise

        logger.info(
            "Резюме загружено: целевая должность='%s'",
            resume.target_position,
        )
        return resume
