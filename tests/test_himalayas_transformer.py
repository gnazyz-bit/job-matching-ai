
"""Tests for Himalayas vacancy transformation."""

import pytest

from job_matching.data.himalayas_transformer import (
    clean_html,
    transform_job,
)


def test_clean_html_paragraphs():
    html = "<p>Python</p><p>SQL</p>"

    assert clean_html(html) == "Python\nSQL"


def test_clean_html_lists():
    html = "<ul><li>Python</li><li>SQL</li></ul>"

    assert clean_html(html) == "Python\nSQL"


def test_clean_html_entities():
    html = "<p>Python &amp; SQL</p>"

    assert clean_html(html) == "Python & SQL"


def test_clean_html_plain_text():
    assert clean_html("Data Analyst") == "Data Analyst"


def test_clean_html_invalid_input():
    with pytest.raises(TypeError):
        clean_html(None)


def test_transform_job():
    job = {
        "guid": "job-123",
        "title": "Data Analyst",
        "description": "<p>Python and SQL required.</p>",
        "companyName": "Example Company",
        "employmentType": "Full Time",
        "seniority": ["Junior"],
        "minSalary": 50000,
        "maxSalary": 70000,
        "currency": "USD",
        "salaryPeriod": "annual",
        "locationRestrictions": ["Worldwide"],
        "categories": ["Data Analyst"],
        "pubDate": "2026-11-19",
        "expiryDate": None,
        "applicationLink": "https://example.com/apply",
    }

    result = transform_job(job)

    assert result["id"] == "job-123"
    assert result["title"] == "Data Analyst"
    assert result["description"] == "Python and SQL required."
    assert result["company"] == "Example Company"
    assert result["salary_from"] == 50000
    assert result["salary_to"] == 70000
    assert result["salary_currency"] == "USD"
    assert result["source"] == "himalayas"


def test_transform_job_missing_title():
    with pytest.raises(ValueError):
        transform_job({"description": "<p>Test</p>"})


def test_transform_job_empty_title():
    with pytest.raises(ValueError):
        transform_job({"title": "   "})


def test_transform_job_invalid_type():
    with pytest.raises(TypeError):
        transform_job("not a dictionary")


def test_transform_job_missing_description():
    result = transform_job({
        "guid": "job-456",
        "title": "Python Developer",
    })

    assert result["description"] == ""


def test_transform_job_preserves_seniority():
    result = transform_job({
        "guid": "job-789",
        "title": "Senior Developer",
        "seniority": ["Senior"],
    })

    assert result["seniority"] == ["Senior"]
