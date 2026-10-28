
# Job Matching AI

A machine learning project for matching candidate resumes with job vacancies based on professional skills, experience, job titles, and salary expectations.

**Project status:** Work in Progress (WIP)

## Project Overview

The goal of this project is to develop a job matching system that:

1. Identifies suitable vacancies for a candidate and explains the matching results.
2. Provides recommendations for improving the candidate's resume.
3. Generates a short cover letter tailored to a selected vacancy.

The project is being developed as part of an internship assignment.

## Data Source

Job vacancies are retrieved from the following API:

https://backend.cap-pvl.kz/api/vacancies

The dataset includes:

- Job title
- Job description
- Salary range
- Qualification
- Company
- Vacancy status
- Creation date

### Data Limitations

During exploratory data analysis, several limitations were identified:

- Job descriptions duplicate job titles.
- Detailed skill requirements are unavailable.
- Experience requirements are not sufficiently specified.
- Qualification information is not detailed enough for comprehensive candidate matching.

These limitations were checked across different API pages.

For further development, synthetic job requirements will be prepared to support matching based on skills and professional experience.

Synthetic requirements will be stored separately from the original API data.

## Current Implementation

The following components have been implemented:

### 1. Vacancy Data Collection

`fetch_vacancies.py`

- Retrieves vacancies from the API.
- Handles paginated API responses.
- Extracts relevant vacancy information.
- Removes duplicate vacancy IDs.
- Saves the dataset as CSV.

### 2. Exploratory Data Analysis

`analyze_vacancies.py`

- Analyzes missing values.
- Examines salary distributions.
- Identifies frequently occurring job titles.
- Checks qualification information.
- Evaluates job description quality.
- Analyzes vacancy creation dates.

### 3. API Data Quality Validation

`check_api_pages.py`

- Checks data from different API pages.
- Compares job descriptions with job titles.
- Examines qualification information.
- Analyzes vacancy dates.

### 4. Job Title Analysis

`check_job_titles.py`

- Searches for potentially relevant job titles using predefined keywords.
- Displays matching vacancies and salary information.

### 5. Synthetic Resume

`resume.json`

A fictional candidate profile containing:

- Target position
- Technical skills
- Professional experience
- Salary expectations
- Education
- Academic projects

### 6. Initial Feature Engineering

`feature_engineering.py`

Implemented methods:

- Job title normalization using a predefined dictionary.
- TF-IDF vectorization.
- Cosine similarity calculation.
- Preliminary vacancy ranking based on job title similarity.
- Exporting calculated similarity scores to CSV.

Currently, similarity is calculated between the candidate's target position and vacancy titles.

## Technologies

- Python
- Pandas
- Requests
- Scikit-learn
- TF-IDF
- Cosine Similarity

## Project Structure

```text
job-matching-ai/
├── data/
│   ├── vacancies.csv
│   ├── vacancies_features.csv
│   └── resume.json
├── fetch_vacancies.py
├── analyze_vacancies.py
├── check_api_pages.py
├── check_job_titles.py
├── load_resume.py
├── feature_engineering.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/
cd job-matching-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Job Matching AI
A learning project for matching fictional candidate resumes with job vacancies.
Developed as an internship assignment.

Status: work in progress. Vacancy collection, data inspection, and initial
feature engineering are implemented. A supervised matching model has not yet
been trained.
Project goal
The completed system should:
1. Recommend suitable vacancies and explain the results.
2. Suggest improvements to the candidate's resume.
3. Generate a short cover letter for a selected vacancy.
The current implementation calculates job title similarity only. It does
not yet decide whether a vacancy is professionally suitable for a candidate.
Implemented features
- Collect all vacancy pages by following the API's hydra:next links.
- Retry temporary HTTP errors and check the downloaded record count against
  the total reported by the API.
- Remove duplicate vacancy IDs and save the data to CSV.
- Replace the saved vacancy CSV only after successful collection and writing.
- Inspect missing values, salaries, qualifications, descriptions, and dates.
- Use two fictional resumes: a junior data analyst and a cook.
- Select the resume file through a command-line argument.
- Normalize selected English target job titles with a small manual dictionary.
- Calculate TF-IDF and cosine similarity between the target position and all
  downloaded vacancy titles.
- Display the top 10 results, including available vacancy IDs, companies, and
  salary fields.
- Save all ranked vacancies separately for each resume filename.
Data source
Vacancies are collected from:

https://backend.cap-pvl.kz/api/vacancies

The loader saves these fields:
Column	Meaning
id	Vacancy identifier from the API; IDs need not be consecutive
title	Job title
description	Description supplied by the API
salary_from	Lower salary field supplied by the API
salary_to	Upper salary field supplied by the API
qualification	Qualification value supplied by the API
company	Organization name
status	Vacancy status supplied by the API
created_at	Creation timestamp supplied by the API


Findings from the inspected full download
These figures describe the inspected snapshot, not a permanent API total:
Measure	Result
Vacancies	31,350
Distinct company names	2,674
Descriptions equal to titles, ignoring case and surrounding spaces	29,025 (92.58%)
Descriptions different from titles	2,325 (7.42%)
Records with qualification = noExperience	31,350


Pandas reported no missing values in the saved columns. However, populated
fields are not necessarily informative: some inspected descriptions only
repeat a title or name the employer's industry.

Dedicated skill and required-experience columns are not present in the saved
CSV. Whether other API fields provide this information still needs to be
checked. Different descriptions do not automatically contain job requirements.

Zero salary values require clarification before salary compatibility is
implemented. They should not automatically be interpreted as a real salary of
zero. Likewise, the uniform noExperience value is not sufficient evidence
that every employer accepts applicants without experience.

Creation dates and API status values alone do not establish that a vacancy is
still accepting applications.
Fictional resumes
All candidate profiles are fictional and are not taken from an applicant database.
File	Target position	Experience	Expected monthly salary
data/resume.json	Junior Data Analyst	0 years	150,000 KZT
data/resume_cook.json	Cook (Повар)	2 years	200,000 KZT


The resumes include skills, education, experience, and projects. At present,
only target_position is used in similarity calculation. Changing the
other resume fields will not change the current scores.
Project structure
job-matching-ai/
├── data/
│   ├── vacancies.csv
│   ├── resume.json
│   ├── resume_cook.json
│   ├── vacancies_features_resume.csv       # generated
│   └── vacancies_features_resume_cook.csv  # generated
├── fetch_vacancies.py
├── analyze_vacancies.py
├── check_api_pages.py
├── check_job_titles.py
├── load_resume.py
├── feature_engineering.py
├── requirements.txt
├── .gitignore
└── README.md
Older project versions may also contain data/vacancies_features.csv. The
updated feature script writes the resume-specific output files shown above;
the older file is not used as its input.
Installation
Clone the repository and enter its directory:
git clone https://github.com/gnazyz-bit/job-matching-ai.git
cd job-matching-ai
Create a virtual environment:
python -m venv .venv
Activate it in Windows PowerShell:
.\.venv\Scripts\Activate.ps1
Or activate it on Linux/macOS:
source .venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Usage
Run the commands below from the project directory.
1. Download or refresh vacancies
python fetch_vacancies.py
This collects all pages and saves data/vacancies.csv. Collection may take a
long time because the API returns a small number of vacancies per page. The
download does not resume after interruption; a new run starts from page one.
If the downloaded count differs from the total reported on the first page,
the loader stops without replacing the previous CSV. Changes to the source
during collection can cause such a mismatch.

Download once, then reuse the saved CSV. Run the loader again when a fresh
snapshot is needed; changing a resume does not require a new API download.
2. Inspect the downloaded data
python analyze_vacancies.py
Optional diagnostic scripts:
python check_api_pages.py
python check_job_titles.py
python load_resume.py
check_api_pages.py makes additional API requests to selected pages.
check_job_titles.py searches the saved CSV with predefined keywords; it does
not determine professional suitability. load_resume.py displays the original
data/resume.json profile.
3. Rank titles for the data analyst resume
python feature_engineering.py data/resume.json
Output: data/vacancies_features_resume.csv.
4. Rank titles for the cook resume
python feature_engineering.py data/resume_cook.json
Output: data/vacancies_features_resume_cook.csv.

Without an argument, the feature script uses data/resume.json:
python feature_engineering.py
Relative resume paths are resolved from the directory containing
feature_engineering.py. Absolute resume paths are also supported. The source
vacancy CSV and generated results are located in that script's data directory.

Output names use the resume filename without its extension. Different resume
filenames therefore produce separate results. Running the same resume again
replaces its previous result; files with the same stem share the same output.
Understanding the current results
The script adds title_similarity to every vacancy, sorts descending, and
prints the first 10 rows. The saved CSV contains all vacancies, including
those with zero similarity. No suitability threshold or filter is applied.

Scores reflect textual overlap, not a probability of suitability. For example,
0.33 does not mean a vacancy is 33% suitable. A chemist-analyst can share the
word аналитик with a data analyst while requiring a different profession.

TF-IDF weights depend on the collection of titles. Scores can therefore change
when the vacancy dataset changes. The manual job-title dictionary applies to
the candidate's target position only; it is not a general translation system.

fit_transform fits the text vectorizer's vocabulary and weights. It does
not train a supervised classifier on examples labelled suitable/unsuitable.
Validation so far
The updated feature script was checked on a small artificial vacancy dataset:
default resume selection, explicit cook resume selection, expected exact-title
ranking, separate output files, and retention of all input rows were verified.

These checks verify basic script behavior. They do not measure matching quality
on real vacancies. An automated project test suite has not yet been added.
Next steps
1. Inspect complete API records for additional skill and experience information.
2. If real requirements are unavailable, prepare a clearly marked synthetic
   demonstration dataset separately from the original API data. Do not present
   invented requirements as actual employer requirements.
3. Add skill, experience, and salary compatibility features, distinguishing
   unknown requirements from mismatches.
4. Prepare resume-vacancy pairs with independently assigned suitable/unsuitable
   labels and short reasons.
5. Train a simple supervised model and evaluate it on held-out examples, keeping
   duplicate or near-duplicate vacancies together when splitting the data.
6. Produce recommendations with explanations and explicit unknowns.
7. Generate resume improvement suggestions and a short cover letter using only
   supported candidate facts.
8. Integrate and test the complete workflow.
The current repository is an initial title-similarity baseline, not a completed
resume-to-vacancy recommendation system.
Run the scripts from the project root directory.

Download vacancies:

```bash
python fetch_vacancies.py
```

Analyze the dataset:

```bash
python analyze_vacancies.py
```

Check API pages:

```bash
python check_api_pages.py
```

Analyze relevant job titles:

```bash
python check_job_titles.py
```

Display the fictional resume:

```bash
python load_resume.py
```

Calculate job title similarity:

```bash
python feature_engineering.py
```

The feature engineering script saves the results to:

`data/vacancies_features.csv`

## Next Steps

The following components are planned:

1. Prepare synthetic job requirements and training examples.
2. Extend feature engineering to include skills, experience, and salary compatibility.
3. Train a machine learning classification model.
4. Evaluate model performance.
5. Rank suitable vacancies and explain matching results.
6. Generate resume improvement recommendations.
7. Generate a short cover letter for a selected vacancy.
8. Integrate the components into a complete pipeline.

## Notes

The project is currently at the data analysis and initial feature engineering stage.

The machine learning classification model has not yet been trained.

Future improvements will focus on expanding the feature set and incorporating more detailed job requirements.
