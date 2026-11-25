from __future__ import annotations


def matching_reasons(row):
    reasons = []
    if float(row["role_overlap"]) >= 0.67:
        reasons.append("target position is closely related")
    if row["matched_skills"]:
        reasons.append("mentioned skills: " + row["matched_skills"])
    if float(row["experience_fit"]) >= 0.7:
        reasons.append("estimated seniority compatibility")
    if float(row["salary_known"]) == 1.0:
        reasons.append("salary was comparable in the same currency and period")
    return reasons or ["limited evidence; review requirements manually"]


def resume_advice(row, resume):
    present = {str(s).lower() for s in resume.get("skills", [])}
    mentioned = [s for s in str(row["mentioned_skills"]).split(", ") if s]
    missing = sorted(s for s in mentioned if s.lower() not in present)
    advice = []
    if missing:
        advice.append("Check whether you actually have the following skills mentioned in the vacancy: " + ", ".join(missing[:6]) + ". Add them only if true; otherwise consider learning them.")
    advice.append("Describe relevant projects and measurable achievements with concrete evidence.")
    advice.append("Tailor the professional summary to the vacancy; never invent skills or experience.")
    return advice
