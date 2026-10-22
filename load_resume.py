
import json
from pathlib import Path

resume_path = Path("data/resume.json")

with open(resume_path, "r", encoding="utf-8") as file:
    resume = json.load(file)

print("=== РЕЗЮМЕ КАНДИДАТА ===")
print("Имя:", resume["name"])
print("Желаемая должность:", resume["target_position"])
print("Навыки:", ", ".join(resume["skills"]))
print("Опыт:", resume["experience_years"], "лет")
print("Ожидаемая зарплата:", resume["expected_salary"], "₸")
