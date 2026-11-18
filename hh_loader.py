"""Download a small, permissioned sample of Kazakhstan vacancies from HeadHunter API.

Run from the project root: python hh_loader.py
"""
import csv
import json
import os
import time
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

import requests

API_BASE = "https://api.hh.ru"
OUTPUT_DIR = Path(__file__).resolve().parent / "data" / "hh"
EMAIL = "nazyz@mail.ru"  
MAX_VACANCIES = 10  # Start small; increase only after confirming API access


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def html_to_text(html):
    parser = TextExtractor()
    parser.feed(html or "")
    return " ".join(unescape(" ".join(parser.parts)).split())


def get_json(session, endpoint, params=None):
    response = session.get(f"{API_BASE}{endpoint}", params=params, timeout=30)
    print(f"GET {endpoint}: HTTP {response.status_code}")
    if response.status_code != 200:
        print("Ответ API:", response.text[:700])
        if response.status_code == 403:
            print("Доступ ограничен. Проверьте требования к OAuth/капче в документации hh.ru.")
        elif response.status_code == 429:
            print("Превышен лимит запросов. Прекратите загрузку и соблюдайте ограничения API.")
        return None
    return response.json()


def main():
    if EMAIL == "your-email@example.com":
        print("Сначала замените EMAIL на свой действующий контактный адрес в hh_loader.py")
        return

    session = requests.Session()
    session.headers.update({"HH-User-Agent": f"JobMatchingAI/1.0 ({EMAIL})"})
    # Optional, if you have a legitimate access token (never commit it):
    token = os.getenv("HH_ACCESS_TOKEN")
    if token:
        session.headers["Authorization"] = f"Bearer {token}"

    params = {"area": 40, "host": "hh.kz", "page": 0, "per_page": MAX_VACANCIES}
    search = get_json(session, "/vacancies", params)
    if search is None:
        print("Файлы не созданы: поисковый запрос не был успешным.")
        return

    items = search.get("items", [])
    print("Всего найдено по запросу:", search.get("found"))
    print("В первой выборке:", len(items))
    if not items:
        print("Список пуст. Измените параметры поиска.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = []
    for item in items:
        vacancy_id = item.get("id")
        if not vacancy_id:
            continue
        details = get_json(session, f"/vacancies/{vacancy_id}", {"host": "hh.kz"})
        if details is None:
            print("Останавливаю сбор подробностей при ошибке API.")
            break
        raw.append(details)
        time.sleep(1)

    if not raw:
        print("Подробности не получены, CSV не создан.")
        return

    raw_path = OUTPUT_DIR / "vacancies_raw.json"
    raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = []
    for vacancy in raw:
        salary = vacancy.get("salary_range") or vacancy.get("salary") or {}
        experience = vacancy.get("experience") or {}
        employer = vacancy.get("employer") or {}
        area = vacancy.get("area") or {}
        skills = vacancy.get("key_skills") or []
        rows.append({
            "id": vacancy.get("id"),
            "title": vacancy.get("name"),
            "description": html_to_text(vacancy.get("description")),
            "key_skills": ", ".join(s.get("name", "") for s in skills if isinstance(s, dict)),
            "experience": experience.get("name"),
            "experience_id": experience.get("id"),
            "salary_from": salary.get("from"),
            "salary_to": salary.get("to"),
            "currency": salary.get("currency"),
            "company": employer.get("name"),
            "area": area.get("name"),
            "published_at": vacancy.get("published_at"),
            "url": vacancy.get("alternate_url"),
        })

    csv_path = OUTPUT_DIR / "vacancies.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Успешно сохранено {len(rows)} вакансий")
    print(f"Исходные данные: {raw_path}")
    print(f"Таблица: {csv_path}")


if __name__ == "__main__":
    main()
