from git import Repo, Actor

# def push_facts_github(repo_path, file_paths, commit_message, remote_name, remote_url, token):
#     # Definir el autor y el committer
#     author = Actor("Stageddat", "chmarc72@gmail.com")
#     committer = Actor("Stageddat", "chmarc72@gmail.com")

#     repo = Repo(repo_path)
#     repo.index.add(file_paths)
#     repo.index.commit(commit_message, author=author, committer=committer)

#     # Incluir el token en la URL del remoto
#     remote_url_with_token = remote_url.replace("https://", f"https://{token}@")

#     try:
#         origin = repo.remote(name=remote_name)
#         # Establecer la URL con el token para el remoto existente
#         origin.set_url(remote_url_with_token)
#     except ValueError:
#         origin = repo.create_remote(remote_name, url=remote_url_with_token)

#     # Hacer push al remoto
#     try:
#         origin.push()
#         # Imprimir un mensaje de éxito
#         print("El push a GitHub fue exitoso.")

#     except Exception as e:
#         print(f"Ocurrió un error al hacer push al remoto: {e}")

import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def push_facts_github(repo_path, file_paths, commit_message, remote_name, remote_url, token):
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