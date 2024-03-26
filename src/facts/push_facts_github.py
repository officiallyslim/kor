from git import Repo, Actor
from config import github_token

def push_facts_github(repo_path, file_paths, commit_message, remote_name, remote_url, token):
    # def autor and mail
    author = Actor("Stageddat", "chmarc72@gmail.com")
    committer = Actor("Stageddat", "chmarc72@gmail.com")

    repo = Repo(repo_path)
    repo.index.add(file_paths)
    repo.index.commit(commit_message, author=author, committer=committer)

    # add token to url
    remote_url_with_token = remote_url.replace("https://", f"https://{github_token}@")

    try:
        origin = repo.remote(name=remote_name)
        # set url to token
        origin.set_url(remote_url_with_token)
    except ValueError:
        origin = repo.create_remote(remote_name, url=remote_url_with_token)

    # push
    try:
        origin.push()
        print("Exit push.")

    except Exception as e:
        print(f"Failed push: {e}")