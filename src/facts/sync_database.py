import re
import json
from config import facts_md_path, island_fact_database_path, added_trivia_path
from src.facts.push_facts_github import push_facts_github
from datetime import datetime
import pytz
import dotenv
import os

dotenv.load_dotenv()
token = str(os.getenv("GITHUB_TOKEN"))

def sync_database():
    with open(facts_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    with open(facts_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    facts_pattern = re.compile(r"^(\d+)\.\s*(.+)$", re.MULTILINE)
    md_facts = {int(idx): fact.strip() for idx, fact in facts_pattern.findall(md_content)}

    with open(island_fact_database_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    ordered_json_data = {}

    for i, (fact_id, fact_text) in enumerate(md_facts.items(), start=1):
        ordered_json_data[str(i)] = {
            "fact": fact_text, 
            "daily": json_data.get(str(fact_id), {}).get("daily", False),
            "img_link": json_data.get(str(fact_id), {}).get("img_link", None),
            "source_link": json_data.get(str(fact_id), {}).get("source_link", None)
        }

    with open(island_fact_database_path, "w", encoding="utf-8") as f:
        json.dump(ordered_json_data, f, indent=4, ensure_ascii=False)

    version_prefix = "**Version: "
    version_suffix = "**"

    # get version
    version_line = next((line for line in lines if line.startswith(version_prefix)), None)
    if version_line is None:
        return "Failed to load local version"

    local_version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))
    est = pytz.timezone('US/Eastern')
    est_time = datetime.now(est).strftime('%H:%M EST')

    with open(facts_md_path, "w", encoding="utf-8") as f:
        f.write("# FACTS LIST\n")
        f.write(f"**Version: {local_version + 1}**\n\n")
        f.write(f"**Updated by: stageddat**\n")
        f.write(f"**Updated at: {est_time}**\n")
        for i, fact in enumerate(md_facts.values(), start=1):
            f.write(f"{i}. {fact}\n")
    push_facts_github('./', [facts_md_path, island_fact_database_path], f'Update sync database', 'kor', 'https://github.com/Stageddat/kor', token)
    return True