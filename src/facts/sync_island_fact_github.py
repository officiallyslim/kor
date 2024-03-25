import requests
from config import (
    facts_md_path,
    github_token,
    raw_added_fact_github,
    raw_daily_count_github,
    raw_fact_database_github,
    raw_fact_list_github,
    island_fact_database_path,
    added_trivia_path,
    daily_count_path,
)
from src.facts.push_facts_github import push_facts_github

async def sync_github_database(github_version, local_version):
    if github_version == local_version:
        return "Already synchronized"

    elif github_version > local_version:
        # Facts list
        headers = {'Authorization': f'token {github_token}'}
        r = requests.get(raw_fact_list_github, allow_redirects=True, headers=headers)
        open(facts_md_path, 'wb').write(r.content)

        # Facts database
        r = requests.get(raw_fact_database_github, allow_redirects=True, headers=headers)
        open(island_fact_database_path, 'wb').write(r.content)

        # Added facts link
        r = requests.get(raw_added_fact_github, allow_redirects=True, headers=headers)
        open(added_trivia_path, 'wb').write(r.content)

        # Daily count
        r = requests.get(raw_daily_count_github, allow_redirects=True, headers=headers)
        open(daily_count_path, 'wb').write(r.content)
        return "Github newer"

    elif github_version < local_version:
        push_facts_github('./', [facts_md_path, added_trivia_path, island_fact_database_path, daily_count_path], f'[BOT] Update fact data from local v:{local_version}', 'kor', 'https://github.com/Stageddat/kor', github_token)
        return "Local newer"
    else:
        await "Error"
