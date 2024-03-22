from getpass import getpass
from git import Repo
import dotenv
import os

def push_facts_github(repo_path, file_paths, commit_message, remote_name, remote_url, token):
    repo = Repo(repo_path)

    repo.index.add(file_paths)

    repo.index.commit(commit_message)

    remote_url_with_token = remote_url.replace("https://", f"https://{token}@")
    
    try:
        origin = repo.remote(name=remote_name)
    except ValueError:
        origin = repo.create_remote(remote_name, url=remote_url_with_token)
    origin.push()