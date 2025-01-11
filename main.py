import json
import argparse

import mlflow
from github import Github


def main(access_token):
    print("[log] Starting the GitHub issue parser.")

    api = Github(access_token)
    repo = api.get_repo("vuejs/core")

    all_labels = [label.name for label in repo.get_labels()]
    open_issues = repo.get_issues(state='open')
    issues = []

    for index, issue in enumerate(open_issues):
        issues.append({
            "title": issue.title,
            "body": issue.body,
            "labels": [label.name for label in issue.labels],
        })
        print(f"\r[log] Parsed {index + 1} issues ...", end="")
    print()

    result_file_path = "dataset.json"
    with open(result_file_path, "w", encoding="utf-8") as file:
        json.dump({
            "project_labels": all_labels,
            "issues": issues,
        }, file)

    print("[log] Finished parsing issues.")

    with mlflow.start_run():
        mlflow.log_artifact(result_file_path)
        print("[log] Logged result as an artifact in MLflow.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Issue Parser")
    parser.add_argument("--access-token", type=str, help="GitHub Access Token")

    args = parser.parse_args()    
    main(args.access_token)
