"""Run the complete Himalayas recommendation and cover-letter workflow."""

from __future__ import annotations

import argparse

from job_matching.services.job_matching_pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Train and run Job Matching AI for Himalayas vacancies")
    parser.add_argument("--resume", default="data/samples/resume_data_analyst.json")
    parser.add_argument("--vacancies", default="data/processed/himalayas_vacancies.csv")
    parser.add_argument("--output", default="data/processed/job_matching_results")
    parser.add_argument("--chosen-rank", type=int, default=1, help="Vacancy rank (1-5) for letter")
    args = parser.parse_args()
    result = run_pipeline(args.resume, args.vacancies, args.output, args.chosen_rank)
    print(result["report"])
    print(f"Training examples: {result['training_count']}; evaluation examples: {result['test_count']}")
    print(f"Ranked matching vacancies: {result['ranked_count']}; output: {args.output}")


if __name__ == "__main__":
    main()
