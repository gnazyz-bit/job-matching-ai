import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Адрес API
BASE_URL = "https://backend.cap-pvl.kz/api/vacancies"

# Пути относительно расположения этого скрипта
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_PATH = DATA_DIR / "vacancies.csv"


def create_session():
    """Создаёт соединение с повторными попытками при временных ошибках."""
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))

    return session


def fetch_all_vacancies():
    """Скачивает все страницы, следуя ссылкам следующей страницы."""
    all_vacancies = []
    visited_urls = set()

    next_url = BASE_URL
    page = 1
    expected_total = None

    with create_session() as session:
        while next_url:
            if next_url in visited_urls:
                raise RuntimeError(
                    "API вернул повторную ссылку на страницу. "
                    "Загрузка остановлена."
                )

            visited_urls.add(next_url)

            print(f"Загружаем страницу {page}...")

            try:
                response = session.get(
                    next_url,
                    timeout=(10, 60),
                )
                response.raise_for_status()
                data = response.json()

            except (requests.RequestException, ValueError) as error:
                raise RuntimeError(
                    f"Ошибка загрузки страницы {page}: {error}"
                ) from error

            if not isinstance(data, dict):
                raise RuntimeError(
                    f"Неожиданный формат ответа на странице {page}."
                )

            vacancies = data.get("hydra:member")

            if not isinstance(vacancies, list):
                raise RuntimeError(
                    f"На странице {page} нет списка hydra:member."
                )

            if not all(isinstance(item, dict) for item in vacancies):
                raise RuntimeError(
                    f"Некорректные записи на странице {page}."
                )

            if page == 1:
                total = data.get("hydra:totalItems")

                if isinstance(total, int) and total >= 0:
                    expected_total = total
                    print(f"API сообщает о {expected_total} вакансиях.")

            all_vacancies.extend(vacancies)

            print(
                f"Получено на странице: {len(vacancies)}. "
                f"Всего получено: {len(all_vacancies)}."
            )

            pagination = data.get("hydra:view") or {}

            if not isinstance(pagination, dict):
                raise RuntimeError(
                    f"Некорректная пагинация на странице {page}."
                )

            next_page = pagination.get("hydra:next")

            if next_page:
                if not isinstance(next_page, str):
                    raise RuntimeError(
                        "API вернул некорректную ссылку следующей страницы."
                    )

                if not vacancies:
                    raise RuntimeError(
                        "API вернул пустую страницу со ссылкой на следующую."
                    )

                next_url = urljoin(response.url, next_page)
                page += 1
                time.sleep(0.2)

            else:
                next_url = None

    if not all_vacancies:
        raise RuntimeError("API не вернул ни одной вакансии.")

    # Проверяем полноту загрузки до сохранения.
    if (
        expected_total is not None
        and len(all_vacancies) != expected_total
    ):
        raise RuntimeError(
            f"Количество записей не совпало: "
            f"ожидалось {expected_total}, "
            f"получено {len(all_vacancies)}. "
            "Возможно, список изменился во время загрузки. "
            "Запустите загрузку повторно."
        )

    return all_vacancies


def prepare_dataframe(vacancies):
    """Выбирает нужные поля и удаляет повторные ID."""
    rows = []

    for vacancy in vacancies:
        if vacancy.get("id") is None:
            raise RuntimeError(
                "Обнаружена вакансия без ID. Проверьте формат данных API."
            )

        organization = vacancy.get("organization")

        if isinstance(organization, dict):
            company = organization.get("name")
        else:
            company = None

        rows.append({
            "id": vacancy["id"],
            "title": (vacancy.get("name") or "").strip(),
            "description": (
                vacancy.get("description") or ""
            ).strip(),
            "salary_from": vacancy.get("salaryFrom"),
            "salary_to": vacancy.get("salaryTo"),
            "qualification": vacancy.get("qualification"),
            "company": company,
            "status": vacancy.get("status"),
            "created_at": vacancy.get("createdAt"),
        })

    df = pd.DataFrame(rows)

    before = len(df)
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    print(f"\nУдалено повторных ID: {before - len(df)}")

    return df


def save_dataframe(df):
    """Заменяет основной CSV только после успешной записи."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    temporary_path = OUTPUT_PATH.with_suffix(".csv.tmp")

    try:
        df.to_csv(
            temporary_path,
            index=False,
            encoding="utf-8-sig",
        )

        temporary_path.replace(OUTPUT_PATH)

    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main():
    vacancies = fetch_all_vacancies()
    df = prepare_dataframe(vacancies)
    save_dataframe(df)

    print("\nЗагрузка завершена!")
    print("Количество уникальных вакансий:", len(df))
    print("Количество компаний:", df["company"].nunique())
    print("Файл сохранён:", OUTPUT_PATH)

    print("\nПервые 5 вакансий:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    try:
        main()

    except (RuntimeError, OSError) as error:
        print(f"\nОшибка: {error}")
        print("Новый CSV не сохранён. Предыдущий файл не заменён.")
        raise SystemExit(1)