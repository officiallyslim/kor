import requests
from config import github_token
from src.global_src.global_raw_links import raw_fact_list_github
from src.global_src.global_path import facts_md_path

async def get_version():
    # Get the github version
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(raw_fact_list_github, headers=headers)
    version_prefix = "**Version: "
    version_suffix = "**"
    content = response.text
    lines = content.split('\n')

    # get version
    version_line = next((line for line in lines if line.startswith(version_prefix)), None)
    if version_line is None:
        return "Failed to connect Github"

    github_version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))

    # Get local version
    with open(facts_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    version_prefix = "**Version: "
    version_suffix = "**"

    # get version
    version_line = next((line for line in lines if line.startswith(version_prefix)), None)
    if version_line is None:
        return "Failed to load local version"

    local_version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))

    return github_version, local_version