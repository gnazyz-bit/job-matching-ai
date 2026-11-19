
import pandas as pd
import re

df = pd.read_csv("data/vacancies.csv")

keywords = [
    "аналитик",
    "анализ данных",
    "data analyst",
    "python",
    "программист",
    "разработчик",
    "информационные технологии"
]

pattern = "|".join(
    re.escape(word) for word in keywords
)

matches = df[
    df["title"].str.contains(
        pattern,
        case=False,
        na=False,
        regex=True
    )
]

print("Всего вакансий:", len(df))
print("Найдено подходящих по ключевым словам:", len(matches))

if not matches.empty:
    print(
        matches[
            ["title", "salary_from", "company"]
        ].to_string(index=False)
    )
else:
    print("В текущем датасете подходящих названий нет.")
