
"""Client for retrieving vacancies from the Himalayas API."""

import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

API_URL = "https://himalayas.app/jobs/api"


class HimalayasClient:
    """Client for the Himalayas remote jobs API."""

    def __init__(self, timeout: int = 20) -> None:
        if timeout <= 0:
            raise ValueError("Timeout must be positive.")

        self.timeout = timeout

    def fetch_page(
        self,
        limit: int = 10,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch and validate one page of vacancies."""

        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100.")

        params: Dict[str, Any] = {"limit": limit}

        if cursor:
            params["cursor"] = cursor

        logger.info(
            "Fetching Himalayas vacancies: limit=%s",
            limit,
        )

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

        except requests.RequestException:
            logger.exception("Himalayas API request failed")
            raise

        except ValueError:
            logger.exception("Invalid JSON response")
            raise

        if not isinstance(data, dict):
            raise ValueError("API response must be an object.")

        if not isinstance(data.get("jobs"), list):
            raise ValueError("API response contains no valid jobs list.")

        next_cursor = data.get("nextCursor")

        if next_cursor is not None and not isinstance(
            next_cursor, str
        ):
            raise ValueError("Invalid pagination cursor.")

        logger.info(
            "Received %s vacancies",
            len(data["jobs"]),
        )

        return data

    def fetch_jobs(
        self,
        max_jobs: int = 100,
        page_size: int = 50,
    ) -> list:
        """Fetch vacancies using cursor-based pagination."""

        if max_jobs <= 0:
            raise ValueError("max_jobs must be positive.")

        if not 1 <= page_size <= 100:
            raise ValueError("page_size must be between 1 and 100.")

        jobs = []
        cursor = None
        seen_cursors = set()

        while len(jobs) < max_jobs:
            limit = min(page_size, max_jobs - len(jobs))

            data = self.fetch_page(
                limit=limit,
                cursor=cursor,
            )

            page_jobs = data["jobs"]
            jobs.extend(page_jobs)

            logger.info(
                "Total collected vacancies: %s/%s",
                len(jobs),
                max_jobs,
            )

            next_cursor = data.get("nextCursor")

            if not page_jobs or not next_cursor:
                break

            if next_cursor == cursor or next_cursor in seen_cursors:
                raise ValueError("Repeated pagination cursor detected.")

            seen_cursors.add(next_cursor)
            cursor = next_cursor

        return jobs[:max_jobs]