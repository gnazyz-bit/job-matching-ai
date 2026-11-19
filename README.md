# Job Matching AI

A Python-based project for matching candidate resumes with job vacancies using text similarity and structured candidate information.

**Project Status:** Work in Progress (WIP)

The project is being developed as part of an internship assignment.

## 1. Project Overview

Job Matching AI aims to help candidates identify relevant job opportunities based on their professional profiles.

The planned system will:

1. Recommend suitable job vacancies.
2. Evaluate compatibility based on skills, experience, education, and salary expectations.
3. Explain vacancy matching results.
4. Suggest improvements to candidate resumes.
5. Generate personalized cover letters for selected vacancies.

The current implementation provides a baseline matching algorithm based on job title similarity using TF-IDF and cosine similarity.

It does not yet evaluate the complete professional suitability of a candidate.

## 2. Data Sources

### 2.1. CAP-PVL API

The initial vacancy dataset was collected from:

https://backend.cap-pvl.kz/api/vacancies

The collected dataset contains the following fields:

| Field | Description |
|---|---|
| id | Vacancy identifier |
| title | Job title |
| description | Vacancy description |
| salary_from | Lower salary value |
| salary_to | Upper salary value |
| qualification | Qualification information |
| company | Employer name |
| status | Vacancy status |
| created_at | Vacancy creation timestamp |

The collected dataset is stored at:

`data/raw/cap_pvl/vacancies.csv`

### 2.2. Himalayas API (Planned)

The next development stage will integrate the Himalayas remote jobs API.

API endpoint:

https://himalayas.app/jobs/api

The purpose of this integration is to obtain more informative vacancy descriptions and investigate the availability of structured job requirements.

Himalayas integration has not yet been implemented.

Future data will be stored separately in:

`data/raw/himalayas/`

## 3. Exploratory Data Analysis

The initial CAP-PVL dataset was analyzed to evaluate its suitability for resume-to-vacancy matching.

### Dataset Summary

| Metric | Result |
|---|---:|
| Total vacancies | 31,350 |
| Distinct companies | 2,674 |
| Descriptions identical to job titles | 29,025 |
| Percentage of duplicated descriptions | 92.58% |
| Descriptions different from job titles | 2,325 |
| Records with qualification = noExperience | 31,350 |

These results describe the collected dataset snapshot, not the current total number of vacancies available through the API.

### Data Quality Limitations

Several important limitations were identified:

- Most vacancy descriptions repeat the job title.
- Detailed skill requirements are generally unavailable.
- Experience requirements are insufficiently specified.
- Qualification information is not reliable enough for comprehensive matching.
- Salary values of zero require further interpretation.
- Vacancy creation dates do not confirm current vacancy availability.

Although the saved dataset contains no missing values in its main columns, populated fields do not necessarily contain meaningful information.

In particular, the value `noExperience` appears in every record. This should not be interpreted as proof that every employer accepts candidates without experience.

### Conclusion

The initial dataset supports baseline job title matching but is insufficient for reliable matching based on professional skills and experience.

More informative vacancy data is required to improve matching quality.

## 4. Current Implementation

The project has been refactored into a modular Python package.

### 4.1. Domain Models

Pydantic models are used to represent and validate structured resume and vacancy data.

Implemented models:

- `Resume`
- `Vacancy`

The models support information such as:

- Target position
- Skills
- Professional experience
- Education
- Salary expectations
- Vacancy title
- Vacancy description
- Employer information

Not all of these fields are currently used by the matching algorithm.

### 4.2. Data Repositories

The project separates data access from matching logic.

**VacancyRepository**

Responsible for:

- Loading vacancy datasets from CSV.
- Validating essential dataset structure.
- Saving processed results.
- Logging data operations.

**ResumeRepository**

Responsible for:

- Loading resumes from JSON.
- Validating resume information using Pydantic.
- Handling invalid or missing files.
- Logging resume loading operations.

### 4.3. Text Preprocessing

The preprocessing module normalizes candidate target positions.

A predefined dictionary translates selected English job titles into Russian equivalents.

For example:

`Data Analyst` → `аналитик данных`

This is a limited normalization mechanism rather than a general translation system.

### 4.4. TF-IDF Similarity

The current baseline uses:

- TF-IDF vectorization.
- Word unigrams and bigrams.
- Cosine similarity.

Similarity is calculated between the candidate's target position and vacancy titles.

The current model does not use vacancy descriptions, skills, experience, education, or salary information in its ranking score.

### 4.5. Vacancy Ranking

Vacancies are sorted in descending order of their calculated title similarity scores.

The system:

1. Loads a resume.
2. Loads vacancy data.
3. Normalizes the candidate's target position.
4. Calculates TF-IDF similarity scores.
5. Ranks vacancies.
6. Displays the top 10 results.
7. Saves the complete ranked dataset to CSV.

### 4.6. Logging and Validation

The refactored implementation includes:

- Structured logging.
- Input validation.
- Error handling.
- Type hints.
- Separation of responsibilities between modules.

## 5. Technologies

The project uses:

- Python 3.9+
- Pandas
- NumPy
- Scikit-learn
- Requests
- Pydantic
- Pytest
- Ruff
- Git

## 6. Project Structure

```text
job-matching-ai/
│
├── archive/
│   ├── check_api_pages.py
│   ├── check_job_titles.py
│   ├── feature_engineering.py
│   ├── feature_engineering_original.py
│   ├── hh_loader.py
│   └── load_resume.py
│
├── data/
│   ├── raw/
│   │   ├── cap_pvl/
│   │   │   └── vacancies.csv
│   │   └── himalayas/
│   │
│   ├── processed/
│   │   ├── vacancies_features_resume_cook.csv
│   │   └── vacancies_features_resume_data_analyst.csv
│   │
│   └── samples/
│       ├── resume_cook.json
│       └── resume_data_analyst.json
│
├── scripts/
│   ├── analyze_vacancies.py
│   ├── compare_models.py
│   └── match_resume.py
│
├── src/
│   └── job_matching/
│       ├── __init__.py
│       ├── config.py
│       │
│       ├── domain/
│       │   ├── __init__.py
│       │   └── models.py
│       │
│       ├── data/
│       │   ├── __init__.py
│       │   ├── repository.py
│       │   ├── resume_repository.py
│       │   └── clients/
│       │       ├── __init__.py
│       │       └── cap_pvl_client.py
│       │
│       ├── matching/
│       │   ├── __init__.py
│       │   ├── preprocessing.py
│       │   ├── similarity.py
│       │   └── ranking.py
│       │
│       └── services/
│           ├── __init__.py
│           └── matching_service.py
│
├── tests/
│   ├── test_matching_service.py
│   ├── test_models.py
│   └── test_repository.py
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

The `archive/` directory contains previous scripts retained for reference.

The main application logic is located in `src/job_matching/`.

## 7. Installation

### Step 1. Clone the Repository

```bash
git clone https://github.com/gnazyz-bit/job-matching-ai.git
cd job-matching-ai
```

### Step 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3. Activate the Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Step 4. Update pip

```bash
python -m pip install --upgrade pip
```

### Step 5. Install the Project

```bash
python -m pip install -e .
```

Editable installation allows the package to be imported without manually configuring `PYTHONPATH`.

### Step 6. Install Development Tools

```bash
python -m pip install pytest ruff
```

## 8. Usage

Run all commands from the project root directory.

### 8.1. Analyze the Original Dataset

```bash
python scripts/analyze_vacancies.py
```

The script displays:

- Total number of vacancies.
- Number of companies.
- Missing values.
- Qualification information.
- Salary statistics.
- Most frequent job titles.
- Description quality.
- Vacancy creation dates.

### 8.2. Match the Data Analyst Resume

```bash
python scripts/match_resume.py
```

The default resume is:

`data/samples/resume_data_analyst.json`

The script loads the original vacancy dataset and calculates job title similarity.

Results are saved to:

`data/processed/vacancies_features_resume_data_analyst.csv`

### 8.3. Match the Cook Resume

```bash
python scripts/match_resume.py --resume data/samples/resume_cook.json
```

Results are saved to:

`data/processed/vacancies_features_resume_cook.csv`

### 8.4. Use a Custom Resume

```bash
python scripts/match_resume.py --resume path/to/resume.json
```

The JSON file must contain a valid candidate profile compatible with the `Resume` model.

### 8.5. Use a Custom Vacancy Dataset

```bash
python scripts/match_resume.py --vacancies path/to/vacancies.csv
```

The vacancy dataset must contain a `title` column.

### 8.6. Compare the Original and Refactored Models

```bash
python scripts/compare_models.py
```

This script compares the baseline scores with previously saved results.

During refactoring, the comparison confirmed:

```text
Количество вакансий: 31350
Оценки совпадают: True
```

This verifies that the refactoring preserved the original TF-IDF similarity scores on the tested dataset.

It does not establish that the ranking is professionally accurate.

## 9. Testing and Code Quality

### Automated Tests

Run:

```bash
python -m pytest tests -q
```

Latest verified result:

```text
17 passed
```

The tests cover:

- Domain model validation.
- Vacancy repository operations.
- Matching service behavior.

Additional tests will be required for future API integrations and new matching features.

### Ruff

Run:

```bash
python -m ruff check src tests scripts
```

Ruff is used to check code quality and identify common Python issues.

Individual scripts can also be checked separately.

## 10. Current Matching Results

The current implementation successfully processes all 31,350 vacancies from the original dataset.

For the example Junior Data Analyst resume, some highly ranked titles include:

- Economist-Analyst
- Programmer-Analyst
- Statistician-Analyst
- Research Analyst
- Financial Analyst

These results demonstrate both the functionality and the limitations of title-based matching.

For example, a Chemist-Analyst vacancy may receive a similarity score because its title includes the word "Analyst", even though its actual professional requirements may be unrelated to data analysis.

The similarity score is not a probability of candidate suitability.

A score of 0.33 does not mean that a candidate is 33% suitable for a vacancy.

The current system provides a baseline for further development rather than a complete recommendation model.

## 11. Refactoring Results

The project was reorganized to improve maintainability, testability, and extensibility.

Completed improvements include:

- Modular package architecture.
- Separation of domain models, repositories, matching algorithms, and services.
- Pydantic validation.
- Structured logging.
- Input validation and error handling.
- Type annotations.
- Automated testing using Pytest.
- Code quality checks using Ruff.
- Centralized configuration of data paths.
- Support for editable package installation.
- Separation of raw data, processed results, and example resumes.
- Preservation of original TF-IDF matching results.

The refactored model was successfully tested against the initial dataset of 31,350 vacancies.

## 12. Next Steps

### 12.1. Himalayas API Integration

Implement a dedicated API client for retrieving remote job vacancies.

The new integration should include:

- API request handling.
- Pagination where supported.
- Error handling and retries.
- Structured logging.
- Response validation.
- Data normalization.
- Storage of raw vacancy data.

The availability and completeness of job requirement fields will be evaluated after integration.

### 12.2. Improved Matching Features

Extend the matching algorithm to consider:

- Job title similarity.
- Required and candidate skills.
- Professional experience.
- Education.
- Salary expectations.

Missing requirements should be treated as unknown rather than automatically interpreted as mismatches.

### 12.3. Matching Quality Evaluation

Prepare independently evaluated resume-vacancy examples.

Compare the existing title-based baseline with improved matching approaches.

Evaluate ranking quality using appropriate metrics and clearly defined evaluation criteria.

### 12.4. Recommendations and Explanations

Develop functionality to:

- Explain why vacancies are recommended.
- Identify missing or partially matching skills.
- Suggest resume improvements.
- Generate short vacancy-specific cover letters.

Generated recommendations must distinguish verified information from assumptions.

### 12.5. Integration Testing

Add tests for:

- Himalayas API client.
- API response parsing.
- Data transformation.
- Skill matching.
- Experience matching.
- Salary compatibility.
- End-to-end matching workflow.

## 13. Project Limitations

The current implementation has several known limitations:

1. Vacancy descriptions in the initial dataset contain insufficient professional requirements.
2. Matching is based only on job title similarity.
3. Candidate skills, experience, education, and expected salary are not yet included in ranking.
4. A supervised suitability classification model has not been trained.
5. Matching quality has not yet been evaluated against independently labeled real-world examples.
6. The Himalayas API integration is planned but not yet implemented.
7. Resume improvement recommendations and cover letter generation are future features.

These limitations are documented to avoid overstating the capabilities of the current system.

## 14. Project Status

**Completed:**

- Initial vacancy data collection.
- Exploratory data analysis.
- Data quality assessment.
- Baseline TF-IDF matching.
- Project architecture refactoring.
- Structured resume and vacancy models.
- Data repositories.
- Logging and input validation.
- Automated tests.
- Model comparison.
- Updated data organization.

**In Progress / Planned:**

- Himalayas API integration.
- Matching by skills and experience.
- Salary and education compatibility.
- Matching quality evaluation.
- Recommendation explanations.
- Resume improvement suggestions.
- Cover letter generation.
