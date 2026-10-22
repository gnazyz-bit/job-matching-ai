
import json
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Загружаем резюме
with open("data/resume.json", "r", encoding="utf-8") as file:
    resume = json.load(file)

# 2. Загружаем вакансии
df = pd.read_csv("data/vacancies.csv")

# 3. Желаемая должность кандидата
# target_position = resume["target_position"]
# Словарь эквивалентных названий профессий
job_titles = {
    "junior data analyst": "аналитик данных",
    "data analyst": "аналитик данных",
    "python developer": "разработчик python",
    "software engineer": "инженер-программист",
    "accountant": "бухгалтер",
    "teacher": "учитель"
}

original_position = resume["target_position"]

target_position = job_titles.get(
    original_position.lower().strip(),
    original_position
)

print("Исходная должность:", original_position)
print("Нормализованная должность:", target_position)

# 4. Формируем список текстов
texts = [target_position] + df["title"].fillna("").tolist()

# 5. Преобразуем названия должностей в TF-IDF векторы
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(texts)

# 6. Рассчитываем сходство с резюме
similarities = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:]
).flatten()

# 7. Добавляем признак
df["title_similarity"] = similarities

# 8. Сортируем вакансии
df = df.sort_values(
    by="title_similarity",
    ascending=False
)

# 9. Выводим ТОП-10
print("=== ТОП-10 ВАКАНСИЙ ПО СХОДСТВУ ===")

print(
    df[["title", "title_similarity"]]
    .head(10)
    .to_string(index=False)
)

# 10. Сохраняем результат
df.to_csv(
    "data/vacancies_features.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nРезультат сохранен в data/vacancies_features.csv")
