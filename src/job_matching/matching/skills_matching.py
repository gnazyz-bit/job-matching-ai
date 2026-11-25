
"""Skill mention matching for Himalayas vacancies."""

import re
from typing import Dict, List

SKILL_PATTERNS = {
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Pandas": r"\bpandas\b",
    "Excel": r"\bexcel\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "Data Analysis": r"\bdata\s+analys(?:is|t|ts)\b",
    "Data Visualization": r"\bdata\s+visuali[sz]ation\b",
    "R": r"\br\b",
    "Spark": r"\bspark\b",
    "Databricks": r"\bdatabricks\b",
    "DAX": r"\bdax\b",
    "Power Query": r"\bpower\s+query\b",
}


def extract_skills(text: str) -> List[str]:
    """Find known skill mentions in vacancy text."""

    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    found = []

    for skill, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(skill)

    return found


def match_skills(
    candidate_skills: List[str],
    vacancy_text: str,
) -> Dict[str, object]:
    """Compare candidate skills with vacancy text mentions."""

    if not isinstance(candidate_skills, list):
        raise TypeError("Candidate skills must be a list.")

    if any(
        not isinstance(skill, str)
        for skill in candidate_skills
    ):
        raise TypeError("Every candidate skill must be a string.")

    vacancy_skills = extract_skills(vacancy_text)

    normalized_candidate = {
        skill.strip().casefold()
        for skill in candidate_skills
        if skill.strip()
    }

    matched = [
        skill
        for skill in vacancy_skills
        if skill.casefold() in normalized_candidate
    ]

    unmatched = [
        skill
        for skill in vacancy_skills
        if skill.casefold() not in normalized_candidate
    ]

    return {
        "detected_skills": vacancy_skills,
        "matched_skills": matched,
        "unmatched_skills": unmatched,
        "matched_count": len(matched),
    }
