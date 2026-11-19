
"""Запуск сопоставления резюме с вакансиями."""

import argparse
import logging
from pathlib import Path

from job_matching.config import (
    CAP_PVL_VACANCIES,
    PROCESSED_DATA_DIR,
    SAMPLES_DIR,
    setup_logging,
)
from job_matching.data.repository import VacancyRepository
from job_matching.data.resume_repository import ResumeRepository
from job_matching.services.matching_service import match_vacancies

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Сопоставление резюме с вакансиями."
    )
    parser.add_argument(
        "--resume",
        type=Path,
        default=SAMPLES_DIR / "resume_data_analyst.json",
        help="Путь к JSON-файлу резюме.",
    )
    parser.add_argument(
        "--vacancies",
        type=Path,
        default=CAP_PVL_VACANCIES,
        help="Путь к CSV-файлу вакансий.",
    )
    args = parser.parse_args()

    setup_logging()

    resume = ResumeRepository().load(args.resume)
    vacancies = VacancyRepository(args.vacancies).load()

    ranked = match_vacancies(
        target_position=resume.target_position,
        vacancies=vacancies,
    )

    output_path = (
        PROCESSED_DATA_DIR
        / f"vacancies_features_{args.resume.stem}.csv"
    )

    VacancyRepository(output_path).save(ranked)

    logger.info("Результаты сохранены: %s", output_path)

    display_columns = [
        col
        for col in [
            "id",
            "title",
            "company",
            "salary_from",
            "salary_to",
            "title_similarity",
        ]
        if col in ranked.columns
    ]

    print("\nТОП-10 ВАКАНСИЙ:")
    print(ranked[display_columns].head(10).to_string(index=False))
    print(
        "\nПримечание: оценка отражает только текстовое "
        "сходство названий должностей."
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError) as error:
        logger.error("Ошибка сопоставления: %s", error)
        raise SystemExit(1) from error
