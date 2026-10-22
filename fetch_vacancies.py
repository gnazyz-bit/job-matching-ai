
import requests
import pandas as pd
import time
from pathlib import Path

# Настройки
BASE_URL = "https://backend.cap-pvl.kz/api/vacancies"
MAX_PAGES = 100

# Папка для данных
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

all_vacancies = []

# Загружаем вакансии постранично
for page in range(1, MAX_PAGES + 1):
    print(f"Загружаем страницу {page}/{MAX_PAGES}")

    try:
        response = requests.get(
            BASE_URL,
            params={"page": page},
            timeout=20
        )
        response.raise_for_status()

        data = response.json()
        vacancies = data.get("hydra:member", [])

        if not vacancies:
            print("Вакансии закончились.")
            break

        all_vacancies.extend(vacancies)
        time.sleep(0.2)

    except requests.RequestException as error:
        print(f"Ошибка на странице {page}: {error}")
        break

# Преобразуем JSON в таблицу
cleaned_vacancies = []

for vacancy in all_vacancies:
    organization = vacancy.get("organization") or {}

    cleaned_vacancies.append({
        "id": vacancy.get("id"),
        "title": (vacancy.get("name") or "").strip(),
        "description": (vacancy.get("description") or "").strip(),
        "salary_from": vacancy.get("salaryFrom"),
        "salary_to": vacancy.get("salaryTo"),
        "qualification": vacancy.get("qualification"),
        "company": organization.get("name"),
        "status": vacancy.get("status"),
        "created_at": vacancy.get("createdAt")
    })

df = pd.DataFrame(cleaned_vacancies)

# Убираем повторения по ID
df = df.drop_duplicates(subset=["id"])

# Сохраняем результат
output_path = DATA_DIR / "vacancies.csv"

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nЗагрузка завершена!")
print("Количество вакансий:", len(df))
print("Количество компаний:", df["company"].nunique())
print("Файл сохранен:", output_path)

print("\nПервые 5 вакансий:")
print(df.head().to_string(index=False))
