
"""Transform Himalayas API data into structured vacancy records."""

from html import unescape
from html.parser import HTMLParser
from typing import Any, Dict


class HTMLTextExtractor(HTMLParser):
    """Extract readable text from HTML."""

    BLOCK_TAGS = {
        "p", "div", "li", "br", "h1", "h2", "h3",
        "h4", "h5", "h6", "ul", "ol", "section",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def get_text(self) -> str:
        lines = "".join(self.parts).splitlines()

        cleaned_lines = [
            " ".join(line.split())
            for line in lines
            if line.strip()
        ]

        return "\n".join(cleaned_lines)


def clean_html(html_content: str) -> str:
    """Convert HTML content into plain text."""

    if not isinstance(html_content, str):
        raise TypeError("HTML content must be a string.")

    parser = HTMLTextExtractor()
    parser.feed(html_content)

    return unescape(parser.get_text())


def transform_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize one Himalayas vacancy."""

    if not isinstance(job, dict):
        raise TypeError("Job must be a dictionary.")

    title = job.get("title")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Job title is required.")

    description = job.get("description") or ""

    return {
        "id": job.get("guid"),
        "title": title.strip(),
        "description": clean_html(description),
        "company": job.get("companyName"),
        "employment_type": job.get("employmentType"),
        "seniority": job.get("seniority"),
        "salary_from": job.get("minSalary"),
        "salary_to": job.get("maxSalary"),
        "salary_currency": job.get("currency"),
        "salary_period": job.get("salaryPeriod"),
        "location_restrictions": job.get("locationRestrictions"),
        "categories": job.get("categories"),
        "published_at": job.get("pubDate"),
        "expires_at": job.get("expiryDate"),
        "url": job.get("applicationLink"),
        "source": "himalayas",
    }
