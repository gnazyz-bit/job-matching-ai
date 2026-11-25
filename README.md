# Job Matching AI

A Python project for ranking job vacancies against structured candidate resumes. The current development focus is remote job data from the **Himalayas API** and an explainable, rule-based matching baseline.

**Status:** Work in Progress (WIP) — internship/learning project.

> **Important:** Matching scores are heuristic ranking signals, **not** probabilities, suitability percentages, or hiring recommendations validated against labeled outcomes.

## 1. Project Goals

The intended system will:

1. Recommend potentially relevant vacancies for a candidate profile.
2. Compare job titles, skills, experience, education, and salary expectations.
3. Explain matching results and identify gaps or unknown requirements.
4. Suggest resume improvements.
5. Generate vacancy-specific cover letters.

Only part of this scope is implemented. The active matching service currently evaluates **job title similarity, skill mentions, and a coarse seniority heuristic**. Education, explicit years-of-experience requirements, and salary compatibility are planned.

## 2. Current Data Source: Himalayas

API endpoint: <https://himalayas.app/jobs/api>

The project includes a client with cursor-based pagination, request/error handling, and response validation, plus a transformer that converts API jobs into a tabular dataset and cleans HTML descriptions.

A locally collected snapshot contains **1,000 vacancies**. This count describes the downloaded snapshot, not the number of jobs currently available through the API.

Data paths:

| Path | Contents |
| --- | --- |
| `data/raw/himalayas/vacancies.json` | Saved raw API jobs |
| `data/processed/himalayas_vacancies.csv` | Transformed vacancy records |
| `data/samples/resume_data_analyst.json` | Example synthetic candidate resume |
| `data/samples/resume_cook.json` | Additional example resume |

The transformed vacancy data includes identifiers, titles, cleaned descriptions, employer names, seniority, employment type, salary fields, location restrictions, categories, publication/expiration dates, URLs, and source information (depending on source availability).

**Caution:** A nonempty field is not necessarily a verified job requirement. Location restrictions and salary fields must be interpreted carefully; a remote role is not automatically open worldwide.

## 3. Implemented Components

### 3.1. Data ingestion and transformation

- `HimalayasClient`: retrieves jobs using the API's cursor pagination.
- `himalayas_transformer.py`: normalizes records and converts descriptions from HTML to readable text.
- `scripts/fetch_himalayas.py`: saves raw and processed vacancy datasets.
- `VacancyRepository`: loads and saves tabular data with basic validation.
- `ResumeRepository`: loads candidate JSON and validates it with the `Resume` model.

### 3.2. Domain models

Pydantic models in `src/job_matching/domain/models.py` represent resumes and vacancies. The resume model supports information including target position, skills, years of experience, education, and salary expectations, though not all fields currently affect ranking.

### 3.3. Himalayas matching service

`src/job_matching/services/himalayas_matching_service.py` exposes `match_himalayas_vacancies(resume, vacancies)`.

Current ranking features:

| Feature | Current approach | Important limitation |
| --- | --- | --- |
| Job title | English-language TF-IDF with word unigrams/bigrams and cosine similarity | Similar titles are not always the same occupation |
| Skills | Regex-based detection and overlap with candidate skills | A mentioned skill is not necessarily required |
| Seniority | Heuristic mapping of candidate years of experience to vacancy seniority labels | Not a comparison with explicit required years |
| Role relevance | Simple title-word overlap used to adjust the combined score | Can overreward broad or ambiguous titles |

The current service computes a weighted base score:

```text
base_score = 0.45 * title_score + 0.35 * skill_score + 0.20 * seniority_score
match_score = base_score * (0.30 + 0.70 * role_score)
```

These weights and heuristics are **provisional**; they have not been optimized or validated on independently labeled resume–vacancy pairs.

The output includes a ranked DataFrame and diagnostic fields such as `title_score`, `skill_score`, `seniority_score`, `role_score`, `match_score`, `matched_skills`, and `other_mentioned_skills`.

## 4. Project Structure

The following is the relevant structure following archival of the previous baseline implementation. Generated caches and virtual environments are omitted.

```text
job-matching-ai/
├── archive/
│   ├── cap_pvl/
│   │   ├── analyze_vacancies.py
│   │   ├── cap_pvl_client.py
│   │   ├── compare_models.py
│   │   ├── match_resume.py
│   │   ├── matching/
│   │   │   ├── matching_service.py
│   │   │   ├── preprocessing.py
│   │   │   ├── ranking.py
│   │   │   └── similarity.py
│   │   └── tests/
│   │       └── test_matching_service.py
│   └── ...                     # Earlier exploratory scripts
├── data/
│   ├── raw/
│   │   ├── cap_pvl/            # Historical dataset
│   │   └── himalayas/
│   │       └── vacancies.json
│   ├── processed/
│   │   ├── himalayas_vacancies.csv
│   │   └── ...                 # Historical outputs
│   └── samples/
│       ├── resume_cook.json
│       └── resume_data_analyst.json
├── scripts/
│   └── fetch_himalayas.py
├── src/job_matching/
│   ├── __init__.py
│   ├── config.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── himalayas_transformer.py
│   │   ├── repository.py
│   │   ├── resume_repository.py
│   │   └── clients/
│   │       ├── __init__.py
│   │       └── himalayas_client.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── matching/
│   │   ├── __init__.py
│   │   └── skills_matching.py
│   └── services/
│       ├── __init__.py
│       └── himalayas_matching_service.py
├── tests/
│   ├── test_himalayas_client.py
│   ├── test_himalayas_transformer.py
│   ├── test_models.py
│   └── test_repository.py
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

The files in `archive/` are retained as project history. **Archived scripts are not guaranteed to run in place:** some still import modules from their former package paths.

## 5. Installation

Requirements: Python **3.9+**, Git, and an internet connection for fetching new API data.

```bash
git clone https://github.com/gnazyz-bit/job-matching-ai.git
cd job-matching-ai
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

Install the package and development tools:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest ruff
```

Dependencies include Pandas, NumPy, Scikit-learn, Requests, and Pydantic. Run commands from the repository root.

## 6. Usage

### 6.1. Fetch Himalayas vacancies

The data collection script is:

```bash
python scripts/fetch_himalayas.py
```

It saves API results under `data/raw/himalayas/` and the transformed CSV under `data/processed/`. Review the script's settings before collecting a new snapshot; API data is subject to change.

### 6.2. Rank vacancies for the example resume

The current Himalayas ranking service is used programmatically; the former `scripts/match_resume.py` belongs to the archived baseline and **must not** be used for Himalayas matching.

From the project root (after editable installation), run in **PowerShell**:

```powershell
@'
import pandas as pd

from job_matching.data.resume_repository import ResumeRepository
from job_matching.services.himalayas_matching_service import match_himalayas_vacancies

resume = ResumeRepository().load("data/samples/resume_data_analyst.json")
vacancies = pd.read_csv("data/processed/himalayas_vacancies.csv")
ranked = match_himalayas_vacancies(resume, vacancies)

print("Total vacancies:", len(vacancies))
print("Ranked vacancies:", len(ranked))
print(ranked[["title", "company", "match_score"]].head(10).to_string(index=False))
'@ | python -
```

The service returns a DataFrame; it does not automatically export the ranked results to a new CSV. To save them, explicitly call `ranked.to_csv(...)` with an appropriate output path.

### 6.3. Synthetic candidate profiles

Candidate profiles are currently represented as JSON validated by the `Resume` model. Synthetic resumes can be varied to explore how the heuristic ranking responds to different titles, skills, and experience levels. Such experiments are useful for development but are **not** a substitute for an independently evaluated test dataset.

## 7. Testing and Code Quality

Run active tests:

```bash
python -m pytest tests -v
```

Check active source and tests:

```bash
python -m ruff check src scripts tests
```

**Last reported local verification (25 November 2026):**

- **34 tests passed**, covering API client behavior, data transformation, domain models, and repository operations.
- **Ruff: `All checks passed!`** after correcting import order.
- **1,000 of 1,000** downloaded vacancies were ranked successfully for the example Data Analyst resume.

**Coverage gap:** the current active test suite does not yet contain dedicated automated tests for the Himalayas ranking heuristics or skill extraction. Those tests should be added as the algorithm evolves.

## 8. Current Matching Example

The last reported run for the synthetic Junior Data Analyst resume produced these top results from the local 1,000-job snapshot:

| Rank | Job title | Company | Match score |
| ---: | --- | --- | ---: |
| 1 | People Data Analyst | RVO Health | 0.4489 |
| 2 | Data Analyst (Power BI & Data Modeling) | K2 Integrity | 0.3966 |
| 3 | 340B Implementation Data Analyst | Pillr Health | 0.3487 |
| 4 | Business Data Analyst | GP Strategies Corporation | 0.2917 |
| 5 | Junior Logistics Analyst | Bamboo Works | 0.2880 |

These are **relative scores within the current heuristic model** and data snapshot. They do not imply verified applicant eligibility, suitability percentages, or that the jobs are still open.

## 9. Previous Baseline and Archive

The project initially explored another vacancy source and a simpler TF-IDF title-matching baseline. Analysis of the historical dataset revealed poor description quality, motivating the switch to richer Himalayas job data.

Old data, scripts, results, and baseline comparisons are retained for traceability under `archive/` and historical data directories. **They are not part of the active Himalayas ranking pipeline.** The README focuses on the current implementation; the archived code is not maintained as a runnable alternative application.

## 10. Known Limitations

1. Mentioned skills are not reliably separated into **required**, **preferred**, and contextual references.
2. Seniority scoring approximates fit from labels; explicit minimum years of experience are not extracted or checked.
3. Education and salary expectations do not yet affect matching scores.
4. Salary values may use different currencies and payment periods; comparisons require normalization and handling of missing information.
5. Geographic eligibility is intentionally deferred; remote positions can still be region-restricted.
6. Title-word overlap can misclassify adjacent but different occupations.
7. The model's heuristic weights have not been calibrated or evaluated against independently labeled matches.
8. Recommendations for resume improvements and cover letters are not implemented.

Missing requirements should be handled as **unknown**, not automatically treated as matches or mismatches.

## 11. Next Steps

1. Extract explicit experience requirements (e.g., minimum years) from job descriptions and distinguish requirements from preferences.
2. Extract and compare education requirements with candidate education.
3. Evaluate salary compatibility, including currency, pay period, missing bounds, and unknown values.
4. Improve skill extraction by distinguishing required skills, preferred skills, and incidental mentions.
5. Introduce focused unit tests for skill, seniority, role, experience, education, and salary scoring.
6. Evaluate ranking quality using independently labeled resume–vacancy pairs and appropriate ranking metrics.
7. Add a dedicated CLI script for Himalayas matching and optional CSV export.
8. Consider geographic eligibility only after clarifying product requirements.
9. Add explainable recommendations, resume feedback, and cover letter generation at later stages.

---

This repository is a **work-in-progress learning project**. Its current results demonstrate an end-to-end data collection and heuristic matching pipeline, not a production-ready recruitment decision system.
