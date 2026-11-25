from __future__ import annotations

import ast
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROLES = {
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI", "Pandas", "Tableau"],
    "Data Engineer": ["Python", "SQL", "Spark", "Databricks", "AWS"],
    "Software Engineer": ["Python", "Java", "JavaScript", "Git", "Docker"],
    "Product Manager": ["Product Management", "Roadmap", "Analytics", "Agile"],
    "Project Manager": ["Project Management", "Agile", "Scrum", "Jira"],
    "Marketing Specialist": ["SEO", "Google Analytics", "Marketing", "Content"],
    "Sales Representative": ["Sales", "CRM", "Salesforce", "Negotiation"],
    "UX Designer": ["Figma", "UX", "UI", "Prototyping"],
    "Customer Support": ["Customer Support", "Zendesk", "Communication"],
    "Financial Analyst": ["Excel", "Financial Modeling", "Finance", "SQL"],
}

SKILL_TERMS = sorted({s for skills in ROLES.values() for s in skills} | {
    "Data Analysis", "Data Visualization", "DAX", "Power Query", "R", "React", "Kubernetes"
}, key=len, reverse=True)
ROLE_STOP = {"junior", "senior", "mid", "level", "lead", "remote", "intern", "associate", "staff", "principal", "ii", "iii", "i"}
FEATURES = ["title_similarity", "role_overlap", "skill_overlap", "experience_fit", "salary_fit", "salary_known"]


def tokens(text):
    return {t for t in re.findall(r"[a-z]+", str(text).lower()) if len(t) > 2 and t not in ROLE_STOP}

def safe_text(value):
    return "" if pd.isna(value) else str(value)

def skills_in(text):
    text = str(text)
    return {s for s in SKILL_TERMS if re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", text, re.I)}

def parse_levels(value):
    if isinstance(value, list):
        return " ".join(str(x) for x in value).lower()
    value = safe_text(value)
    try:
        decoded = ast.literal_eval(value)
        if isinstance(decoded, list):
            return " ".join(str(x) for x in decoded).lower()
    except (ValueError, SyntaxError):
        pass
    return value.lower()

def experience_fit(years, level):
    level = parse_levels(level)
    years = float(years or 0)
    if any(s in level for s in ("director", "executive")):
        threshold = 8
    elif any(s in level for s in ("senior", "lead")):
        threshold = 5
    elif any(s in level for s in ("mid-level", "mid level", "manager")):
        threshold = 2
    elif any(s in level for s in ("entry", "junior", "intern")):
        threshold = 0
    else:
        return 0.5
    return 1.0 if years >= threshold else max(0.0, years / max(threshold, 1))

def salary_fit(expected, expected_currency, vacancy):
    """Only compare like-for-like currency; resume expectation assumed monthly."""
    amount = float(expected or 0)
    if not amount:
        return 0.5, 0.0
    currency = str(expected_currency or "").strip().upper()
    vc = safe_text(vacancy.get("salary_currency", "")).upper()
    if not currency or not vc or currency != vc:
        return 0.5, 0.0
    period = safe_text(vacancy.get("salary_period", "")).lower()
    top = pd.to_numeric(vacancy.get("salary_to"), errors="coerce")
    bottom = pd.to_numeric(vacancy.get("salary_from"), errors="coerce")
    upper = top if pd.notna(top) else bottom
    if pd.isna(upper) or upper <= 0:
        return 0.5, 0.0
    if "annual" in period or "year" in period:
        upper = upper / 12
    elif "month" not in period:
        return 0.5, 0.0
    return (1.0 if amount <= upper else max(0.0, upper / amount)), 1.0

def create_profiles(real):
    profiles = []
    for role, role_skills in ROLES.items():
        for years in (0, 3, 7):
            profiles.append({"target_position": ("Junior " if years == 0 else "") + role,
                             "skills": role_skills[: (3 if years == 0 else len(role_skills))],
                             "experience_years": years,
                             "expected_salary": 2500 if years == 0 else (4500 if years == 3 else 7500),
                             "salary_currency": "USD"})
    profiles.append(real)
    return profiles

def create_features(profiles, df):
    titles = df["title"].fillna("").astype(str).tolist()
    target_positions = [r["target_position"] for r in profiles]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(titles + target_positions)
    similarity = cosine_similarity(matrix[len(titles):], matrix[:len(titles)])
    vacancy_skills = [skills_in(safe_text(v)) for v in df["description"].tolist()]
    vacancy_levels = [parse_levels(v) for v in df["seniority"].tolist()] if "seniority" in df else [""] * len(df)
    records = []
    for person_index, resume in enumerate(profiles):
        own_tokens = tokens(resume["target_position"])
        owned_skills = {s.lower() for s in resume.get("skills", [])}
        for vacancy_index, (_, vacancy) in enumerate(df.iterrows()):
            vac_tokens = tokens(vacancy["title"])
            normalized_role = " ".join(re.findall(r"[a-z]+", str(resume["target_position"]).lower()))
            normalized_role = " ".join(t for t in normalized_role.split() if t not in ROLE_STOP)
            vacancy_words = " ".join(re.findall(r"[a-z]+", str(vacancy["title"]).lower()))
            exact_role = bool(normalized_role and re.search(r"(?<!\w)" + re.escape(normalized_role) + r"(?!\w)", vacancy_words))
            overlap = 1.0 if exact_role else len(own_tokens & vac_tokens) / max(len(own_tokens | vac_tokens), 1)
            mentioned = vacancy_skills[vacancy_index]
            matched = sorted((s for s in mentioned if s.lower() in owned_skills), key=str.lower)
            skill_overlap = len(matched) / max(len(owned_skills), 1)
            sf, sk = salary_fit(resume.get("expected_salary"), resume.get("salary_currency"), vacancy)
            records.append({"profile_id": person_index, "vacancy_id": vacancy_index,
                            "title_similarity": float(similarity[person_index, vacancy_index]),
                            "role_overlap": float(overlap), "skill_overlap": float(skill_overlap),
                            "experience_fit": experience_fit(resume.get("experience_years", 0), vacancy_levels[vacancy_index]),
                            "salary_fit": sf, "salary_known": sk,
                            "matched_skills": ", ".join(matched),
                            "mentioned_skills": ", ".join(sorted(mentioned, key=str.lower))})
    return pd.DataFrame.from_records(records)
