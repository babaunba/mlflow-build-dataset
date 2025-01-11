import json
import argparse

import mlflow
from github import Github

mlflow.autolog(disable=True)

def main(access_token, mlflow_server_uri, repository_name):
    print("[log] Starting the GitHub issue parser.")

    api = Github(access_token)
    repo = api.get_repo(repository_name)

    all_labels = [label.name for label in repo.get_labels()]
    open_issues = repo.get_issues(state='open')
    issues = []
    contributors = []

    for index, issue in enumerate(open_issues):
        issues.append({
            "title": issue.title,
            "body": issue.body,
            "labels": [label.name for label in issue.labels],
            "creator": issue.user.login,
        })
        print(f"\r[log] Parsed {index + 1} issues ...", end="")
    print()

    for index, contributor in enumerate(repo.get_contributors()):
        contributors.append(contributor.login)
        print(f"\r[log] Parsed {index + 1} contributors ...", end="")
    print()

    result_file_path = "dataset.json"
    with open(result_file_path, "w", encoding="utf-8") as file:
        json.dump({
            "repository": repository_name,
            "project_labels": all_labels,
            "issues": issues,
            "contributors": contributors,
        }, file)

    print("[log] Finished parsing issues.")

    mlflow.set_tracking_uri(mlflow_server_uri)
    with mlflow.start_run():
        mlflow.log_artifact(result_file_path)
        print("[log] Logged result as an artifact in MLflow.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub Issue Parser")
    parser.add_argument("--access-token", type=str, help="GitHub Access Token")
    parser.add_argument("--repository", type=str, help="Path to GitHub project")
    parser.add_argument(
        "--mlflow-server",
        type=str,
        help="URI to MLFLow server",
        default="http://localhost:8080",
    )

    args = parser.parse_args()    
    main(args.access_token, args.mlflow_server, args.repository)
