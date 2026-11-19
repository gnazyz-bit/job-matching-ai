
"""Сравнение новой модели с результатами старой TF-IDF."""


import numpy as np
import pandas as pd

from job_matching.config import (
    CAP_PVL_VACANCIES,
    PROCESSED_DATA_DIR,
)
from job_matching.services.matching_service import match_vacancies


def main() -> None:
    
    vacancies_path = CAP_PVL_VACANCIES
    previous_result_path = (
        PROCESSED_DATA_DIR / "vacancies_features_resume_data_analyst.csv"
    )
    vacancies = pd.read_csv(vacancies_path)
    previous = pd.read_csv(previous_result_path)

    current = match_vacancies("Data Analyst", vacancies)

    required_columns = {"id", "title_similarity"}

    if not required_columns.issubset(previous.columns):
        raise ValueError("В старых результатах отсутствуют нужные столбцы.")

    if not required_columns.issubset(current.columns):
        raise ValueError("В новых результатах отсутствуют нужные столбцы.")

    old_scores = previous.set_index("id")["title_similarity"]
    new_scores = current.set_index("id")["title_similarity"]

    if not old_scores.index.is_unique or not new_scores.index.is_unique:
        raise ValueError("Обнаружены повторяющиеся ID вакансий.")

    if set(old_scores.index) != set(new_scores.index):
        raise ValueError("Списки ID вакансий не совпадают.")

    old_scores = old_scores.sort_index()
    new_scores = new_scores.sort_index()

    equal = np.allclose(
        old_scores.to_numpy(),
        new_scores.to_numpy(),
        rtol=1e-9,
        atol=1e-12,
    )

    print("Количество вакансий:", len(current))
    print("Оценки совпадают:", equal)

    print("\nТОП-10 НОВОЙ МОДЕЛИ:")
    print(
        current[
            ["id", "title", "title_similarity"]
        ].head(10).to_string(index=False)
    )

    if not equal:
        raise AssertionError(
            "Новая модель отличается от предыдущей."
        )


if __name__ == "__main__":
    main()
