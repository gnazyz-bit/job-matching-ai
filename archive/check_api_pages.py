
import requests
import pandas as pd

BASE_URL = "https://backend.cap-pvl.kz/api/vacancies"

# Проверяем разные части API
pages = [1, 100, 500, 1000, 2000, 3000, 3135]

results = []

for page in pages:
    try:
        response = requests.get(
            BASE_URL,
            params={"page": page},
            timeout=20
        )
        response.raise_for_status()

        data = response.json()
        vacancies = data.get("hydra:member", [])

        for vacancy in vacancies:
            title = (vacancy.get("name") or "").strip()
            description = (
                vacancy.get("description") or ""
            ).strip()

            results.append({
                "page": page,
                "title": title,
                "qualification": vacancy.get("qualification"),
                "description_length": len(description),
                "has_detailed_description": (
                    description.lower() != title.lower()
                    and len(description) > 0
                ),
                "created_at": vacancy.get("createdAt"),
                "salary_from": vacancy.get("salaryFrom")
            })

        print(f"Страница {page}: получено {len(vacancies)}")

    except requests.RequestException as error:
        print(f"Ошибка на странице {page}: {error}")

df = pd.DataFrame(results)

if df.empty:
    print("Не удалось получить вакансии.")
else:
    print("\n=== АНАЛИЗ РАЗНЫХ СТРАНИЦ ===")

    summary = df.groupby("page").agg(
        count=("title", "count"),
        detailed_descriptions=(
            "has_detailed_description", "sum"
        ),
        qualifications=("qualification", "nunique"),
        average_description_length=(
            "description_length", "mean"
        )
    )

    print(summary.to_string())

    print("\n=== КВАЛИФИКАЦИИ ===")
    print(df["qualification"].value_counts(dropna=False))

    df["created_at"] = pd.to_datetime(
        df["created_at"], errors="coerce", utc=True
    )

    print("\n=== ДАТЫ ===")
    print("Самая старая:", df["created_at"].min())
    print("Самая новая:", df["created_at"].max())
