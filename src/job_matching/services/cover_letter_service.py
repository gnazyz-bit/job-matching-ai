from __future__ import annotations

from job_matching.ml.features import safe_text


def create_cover_letter(resume, vacancy, matched_skills):
    """Evidence-constrained cover letter; never assumes missing experience."""
    company = safe_text(vacancy.get("company")) or "the hiring team"
    name = str(resume.get("name") or "Candidate")
    target = str(vacancy["title"])
    skills = [x for x in str(matched_skills).split(", ") if x]
    evidence = (
        "My listed skills include " + ", ".join(skills[:3]) + "."
        if skills else "I would welcome the opportunity to discuss my relevant skills."
    )
    return (
        f"Dear Hiring Team at {company},\n\n"
        f"I am applying for the {target} position. {evidence}\n"
        "I would appreciate the opportunity to discuss how I could contribute to your team.\n\n"
        f"Best regards,\n{name}"
    )
