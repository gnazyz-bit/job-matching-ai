
"""Download and save vacancies from the Himalayas API."""

import argparse
import json
import logging

import pandas as pd

from job_matching.config import (
    HIMALAYAS_DATA_DIR,
    PROCESSED_DATA_DIR,
    setup_logging,
)
from job_matching.data.clients.himalayas_client import HimalayasClient
from job_matching.data.himalayas_transformer import transform_job

logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Himalayas vacancies."
    )
    parser.add_argument(
        "--max-jobs",
        type=int,
        default=100,
        help="Maximum number of vacancies to download.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=50,
        help="Number of vacancies per API request.",
    )
    args = parser.parse_args()

    setup_logging()

    client = HimalayasClient()

    logger.info("Starting Himalayas download")

    jobs = client.fetch_jobs(
        max_jobs=args.max_jobs,
        page_size=args.page_size,
    )

    if not jobs:
        raise ValueError("No vacancies received from Himalayas.")

    HIMALAYAS_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    raw_path = HIMALAYAS_DATA_DIR / "vacancies.json"

    with raw_path.open("w", encoding="utf-8") as file:
        json.dump(
            jobs,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logger.info("Raw vacancies saved to %s", raw_path)

    transformed = [transform_job(job) for job in jobs]

    dataframe = pd.DataFrame(transformed)

    processed_path = (
        PROCESSED_DATA_DIR / "himalayas_vacancies.csv"
    )

    dataframe.to_csv(
        processed_path,
        index=False,
        encoding="utf-8-sig",
    )

    logger.info(
        "Processed vacancies saved to %s",
        processed_path,
    )

    print("\nDOWNLOAD COMPLETED")
    print("Vacancies:", len(dataframe))
    print("Raw JSON:", raw_path)
    print("Processed CSV:", processed_path)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError) as error:
        logger.error("Download failed: %s", error)
        raise SystemExit(1) from error
