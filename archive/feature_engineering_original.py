import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

# Ручной словарь названий для желаемой должности кандидата.
JOB_TITLES = {
    "junior data analyst": "аналитик данных",
    "data analyst": "аналитик данных",
    "python developer": "разработчик python",
    "software engineer": "инженер-программист",
    "accountant": "бухгалтер",
    "teacher": "учитель",
    "cook": "повар",
    "chef": "шеф-повар",
}


def main():
    parser = argparse.ArgumentParser(
        description="Расчёт текстового сходства должности и названий вакансий."
    )
    parser.add_argument(
        "resume_path",
        nargs="?",
        default="data/resume_data_analyst.json",
        help="Путь к JSON-резюме относительно папки проекта или абсолютный путь.",
    )
    args = parser.parse_args()

    # Папкой проекта считается папка, в которой находится этот скрипт.
    resume_path = Path(args.resume_path).expanduser()
    if not resume_path.is_absolute():
        resume_path = PROJECT_DIR / resume_path

    with resume_path.open("r", encoding="utf-8-sig") as file:
        resume = json.load(file)

    if not isinstance(resume, dict):
        raise ValueError("Резюме должно быть JSON-объектом.")

    original_position = resume.get("target_position")
    if not isinstance(original_position, str) or not original_position.strip():
        raise ValueError("В резюме должно быть непустое поле target_position.")

    original_position = original_position.strip()
    target_position = JOB_TITLES.get(
        original_position.lower(), original_position
    )

    df = pd.read_csv(DATA_DIR / "vacancies.csv")
    if "title" not in df.columns:
        raise ValueError("В vacancies.csv отсутствует столбец title.")
    if df.empty:
        raise ValueError("В vacancies.csv нет вакансий.")

    print("Используемое резюме:", resume_path)
    print("Исходная должность:", original_position)
    print("Нормализованная должность:", target_position)
    print("Количество вакансий:", len(df))

    # Сравниваем только желаемую должность и названия вакансий.
    # Навыки, опыт и зарплата на этом этапе ещё не учитываются.
    texts = [target_position] + df["title"].fillna("").astype(str).tolist()

    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)

    df["title_similarity"] = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:]
    ).flatten()

    # При равных оценках сохраняем исходный порядок вакансий.
    df = df.sort_values(
        by="title_similarity", ascending=False, kind="stable"
    )

    print("\n=== ТОП-10 ВАКАНСИЙ ПО СХОДСТВУ НАЗВАНИЙ ===")
    display_columns = [
        column
        for column in [
            "id", "title", "company", "salary_from", "salary_to",
            "title_similarity",
        ]
        if column in df.columns
    ]
    print(df[display_columns].head(10).to_string(index=False))

    # Сохраняем ВСЕ вакансии, а не только первые десять.
    output_path = DATA_DIR / f"vacancies_features_{resume_path.stem}.csv"
    temporary_path = output_path.with_suffix(".csv.tmp")
    try:
        df.to_csv(temporary_path, index=False, encoding="utf-8-sig")
        temporary_path.replace(output_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    print("\nРезультат сохранён в", output_path)
    print("Оценка отражает сходство названий, а не процент пригодности.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"\nОшибка: {error}")
        raise SystemExit(1)