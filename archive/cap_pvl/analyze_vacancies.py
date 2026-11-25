import pandas as pd

from job_matching.config import CAP_PVL_VACANCIES

# 1. Загружаем данные
df = pd.read_csv(CAP_PVL_VACANCIES)

print("=== ОБЩАЯ ИНФОРМАЦИЯ ===")
print("Количество вакансий:", len(df))
print("Количество компаний:", df["company"].nunique())

# 2. Проверяем пропущенные значения
print("\n=== ПРОПУЩЕННЫЕ ЗНАЧЕНИЯ ===")
print(df.isnull().sum())

# 3. Проверяем квалификацию
print("\n=== ТРЕБОВАНИЯ К КВАЛИФИКАЦИИ ===")
print(df["qualification"].value_counts(dropna=False))

# 4. Анализируем зарплаты
print("\n=== ЗАРПЛАТЫ ===")
print(df[["salary_from", "salary_to"]].describe())

# 5. Самые распространенные должности
print("\n=== ТОП-15 ДОЛЖНОСТЕЙ ===")
print(df["title"].value_counts().head(15))

# 6. Проверяем качество описаний
df["description"] = df["description"].fillna("")
df["title"] = df["title"].fillna("")

same_description = (
    df["description"].str.strip().str.lower()
    == df["title"].str.strip().str.lower()
)

print("\n=== КАЧЕСТВО ОПИСАНИЙ ===")
print("Описание совпадает с названием:",
      same_description.sum())

print("Доля таких вакансий:",
      round(same_description.mean() * 100, 2), "%")

# 7. Проверяем даты
df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce",
    utc=True
)

print("\n=== ДАТЫ СОЗДАНИЯ ===")
print("Самая старая:", df["created_at"].min())
print("Самая новая:", df["created_at"].max())

print("\nКоличество вакансий по годам:")
print(df["created_at"].dt.year.value_counts().sort_index())
