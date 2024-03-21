from git import Repo

def push_facts_github(repo_path, file_paths, commit_message, remote_name, remote_url):
    repo = Repo(repo_path)

    repo.index.add(file_paths)

    repo.index.commit(commit_message)

    try:
        origin = repo.remote(name=remote_name)
    except ValueError:
        origin = repo.create_remote(remote_name, url=remote_url)
    origin.push()
