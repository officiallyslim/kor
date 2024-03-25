import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def push_facts_github(file_paths, commit_message):
    repo_name = "kor"
    branch = "main"
    github_token = os.getenv("GITHUB_TOKEN")
    files_updated = []

    for file_path in file_paths:
        api_url = f"https://api.github.com/repos/Stageddat/{repo_name}/contents/{file_path}"

        get_response = requests.get(api_url, headers={"Authorization": f"token {github_token}"})
        file_content = get_response.json()

        with open(file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("utf-8")

        payload = {
            "message": commit_message,
            "content": encoded_content,
            "sha": file_content.get("sha", ""),
            "branch": branch
        }

        put_response = requests.put(api_url, json=payload, headers={"Authorization": f"token {github_token}"})

        if put_response.status_code == 200 or put_response.status_code == 201:
            files_updated.append(file_path)
        else:
            print(f"Failed uploading: {file_path} - {put_response.json()['message']}")

    if files_updated:
        print(f"Files pushed '{repo_name}': {', '.join(files_updated)}")
    else:
        print(f"Failed push '{repo_name}'.")