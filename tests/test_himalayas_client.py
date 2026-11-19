
"""Tests for the Himalayas API client."""

from unittest.mock import Mock, patch

import pytest
import requests

from job_matching.data.clients.himalayas_client import HimalayasClient


def test_invalid_timeout():
    with pytest.raises(ValueError):
        HimalayasClient(timeout=0)


@pytest.mark.parametrize("limit", [0, -1, 101])
def test_invalid_page_limit(limit):
    client = HimalayasClient()

    with pytest.raises(ValueError):
        client.fetch_page(limit=limit)


@patch("job_matching.data.clients.himalayas_client.requests.get")
def test_fetch_page(mock_get):
    response = Mock()
    response.json.return_value = {
        "jobs": [{"title": "Data Analyst"}],
        "nextCursor": "cursor123",
    }
    mock_get.return_value = response

    client = HimalayasClient()
    result = client.fetch_page(limit=1)

    assert len(result["jobs"]) == 1
    assert result["nextCursor"] == "cursor123"

    mock_get.assert_called_once_with(
        "https://himalayas.app/jobs/api",
        params={"limit": 1},
        timeout=20,
    )


@patch("job_matching.data.clients.himalayas_client.requests.get")
def test_invalid_api_response(mock_get):
    response = Mock()
    response.json.return_value = {"invalid": []}
    mock_get.return_value = response

    with pytest.raises(ValueError):
        HimalayasClient().fetch_page()


@patch("job_matching.data.clients.himalayas_client.requests.get")
def test_http_error(mock_get):
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError(
        "Server error"
    )
    mock_get.return_value = response

    with pytest.raises(requests.HTTPError):
        HimalayasClient().fetch_page()


def test_cursor_pagination():
    client = HimalayasClient()

    responses = [
        {
            "jobs": [{"guid": "1"}, {"guid": "2"}],
            "nextCursor": "cursor1",
        },
        {
            "jobs": [{"guid": "3"}, {"guid": "4"}],
            "nextCursor": "cursor2",
        },
        {
            "jobs": [{"guid": "5"}],
            "nextCursor": None,
        },
    ]

    with patch.object(
        client,
        "fetch_page",
        side_effect=responses,
    ) as mock_fetch:
        jobs = client.fetch_jobs(max_jobs=5, page_size=2)

    assert len(jobs) == 5
    assert [job["guid"] for job in jobs] == [
        "1", "2", "3", "4", "5"
    ]

    assert mock_fetch.call_count == 3

    assert mock_fetch.call_args_list[0].kwargs == {
        "limit": 2,
        "cursor": None,
    }
    assert mock_fetch.call_args_list[1].kwargs == {
        "limit": 2,
        "cursor": "cursor1",
    }
    assert mock_fetch.call_args_list[2].kwargs == {
        "limit": 1,
        "cursor": "cursor2",
    }


def test_repeated_cursor():
    client = HimalayasClient()

    responses = [
        {"jobs": [{"guid": "1"}], "nextCursor": "same"},
        {"jobs": [{"guid": "2"}], "nextCursor": "same"},
    ]

    with patch.object(
        client,
        "fetch_page",
        side_effect=responses,
    ):
        with pytest.raises(
            ValueError,
            match="Repeated pagination cursor",
        ):
            client.fetch_jobs(max_jobs=10, page_size=2)


def test_invalid_max_jobs():
    with pytest.raises(ValueError):
        HimalayasClient().fetch_jobs(max_jobs=0)


def test_invalid_page_size():
    with pytest.raises(ValueError):
        HimalayasClient().fetch_jobs(page_size=101)
