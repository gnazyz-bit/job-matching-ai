
"""Experimental resume matching service for Himalayas vacancies."""
import ast
from typing import List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from job_matching.domain.models import Resume
from job_matching.matching.skills_matching import match_skills


def calculate_title_scores(
    candidate_title: str,
    vacancy_titles: List[str],
) -> List[float]:
    """Calculate English job title similarity using TF-IDF."""

    if not vacancy_titles:
        return []

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )

    documents = [candidate_title] + vacancy_titles

    matrix = vectorizer.fit_transform(documents)

    scores = cosine_similarity(
        matrix[0:1],
        matrix[1:],
    ).flatten()

    return scores.tolist()



def calculate_seniority_score(
    experience_years: float,
    seniority: object,
) -> float:
    """Estimate compatibility with vacancy seniority."""

    if isinstance(seniority, str):
        try:
            seniority = ast.literal_eval(seniority)
        except (ValueError, SyntaxError):
            seniority = [seniority]

    if not isinstance(seniority, (list, tuple)):
        return 0.5

    levels = {
        str(level).strip().casefold()
        for level in seniority
    }

    if experience_years < 1:
        if levels & {"entry-level", "internship", "junior"}:
            return 1.0

        if levels & {"mid-level", "mid"}:
            return 0.4

        if levels & {
            "senior",
            "lead",
            "manager",
            "director",
            "executive",
        }:
            return 0.0

    if experience_years < 3:
        if levels & {"entry-level", "junior", "mid-level"}:
            return 1.0

        if levels & {"senior", "lead"}:
            return 0.3

    if experience_years >= 3:
        if levels & {"mid-level", "senior"}:
            return 1.0

    return 0.5


def match_himalayas_vacancies(
    resume: Resume,
    vacancies: pd.DataFrame,
) -> pd.DataFrame:
    """Rank Himalayas vacancies using title and skill mentions."""

    required_columns = {"title", "description"}

    if not required_columns.issubset(vacancies.columns):
        raise ValueError(
            "Vacancies must contain title and description."
        )

    if vacancies.empty:
        return vacancies.copy()

    title_scores = calculate_title_scores(
        resume.target_position,
        vacancies["title"].fillna("").astype(str).tolist(),
    )

    results: List[dict] = []

    candidate_skill_count = len({
        skill.strip().casefold()
        for skill in resume.skills
        if skill.strip()
    })

    for (_, job), title_score in zip(
        vacancies.iterrows(),
        title_scores,
    ):
        description = (
            job["description"]
            if isinstance(job["description"], str)
            else ""
        )

        skills_result = match_skills(
            resume.skills,
            description,
        )

        matched_count = skills_result["matched_count"]

        skill_score = (
            matched_count / candidate_skill_count
            if candidate_skill_count > 0
            else 0.0
        )

        experience_years = resume.experience_years

        seniority_score = (
            calculate_seniority_score(
                experience_years,
                job.get("seniority"),
            )
            if experience_years is not None
            else 0.5
        )

        final_score = (
            0.45 * title_score
            + 0.35 * skill_score
            + 0.20 * seniority_score
        )

        result = job.to_dict()

        result.update({
            "title_score": round(title_score, 4),
            "skill_score": round(skill_score, 4),
            "match_score": round(final_score, 4),
            "matched_skills": ", ".join(
                skills_result["matched_skills"]
            ),
            "seniority_score": round(seniority_score, 4),
            "other_mentioned_skills": ", ".join(
                skills_result["unmatched_skills"]
            ),
        })

        results.append(result)

    ranked = pd.DataFrame(results)

    return ranked.sort_values(
        "match_score",
        ascending=False,
        kind="stable",
    ).reset_index(drop=True)
