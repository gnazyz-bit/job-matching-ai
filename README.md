
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
