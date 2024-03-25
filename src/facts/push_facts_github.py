from git import Repo, Actor

def push_facts_github(repo_path, file_paths, commit_message, remote_name, remote_url, token):
    # Definir el autor y el committer
    author = Actor("Stageddat", "chmarc72@gmail.com")
    committer = Actor("Stageddat", "chmarc72@gmail.com")

    repo = Repo(repo_path)
    repo.index.add(file_paths)
    repo.index.commit(commit_message, author=author, committer=committer)

    # Incluir el token en la URL del remoto
    remote_url_with_token = remote_url.replace("https://", f"https://{token}@")

    try:
        origin = repo.remote(name=remote_name)
        # Establecer la URL con el token para el remoto existente
        origin.set_url(remote_url_with_token)
    except ValueError:
        origin = repo.create_remote(remote_name, url=remote_url_with_token)

    # Hacer push al remoto
    try:
        origin.push()
        # Imprimir un mensaje de éxito
        print("El push a GitHub fue exitoso.")

    except Exception as e:
        print(f"Ocurrió un error al hacer push al remoto: {e}")