from better_profanity import profanity
import requests
import random
import json
from config import island_fact_database_path, facts_md_path, added_trivia_path, daily_count_path
from src.facts.push_facts_github import push_facts_github
import os
import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# API REQUEST
def get_randomfact():
    url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'
    profanity.load_censor_words()
    try:
        response = requests.get(url)
        response.raise_for_status()
        fact = response.json()
        fact_text = fact['text'].replace("`", "\'")
        if profanity.contains_profanity(fact_text):
            print(f"Inappropriate fact: {fact_text}")
            return get_randomfact()
        else:
            return fact_text
    except requests.exceptions.RequestException as e:
        print(f'Can\'t get random facts.\nError:`{e}`')
        return None

def get_randomcatfact():
    url = 'https://catfact.ninja/fact'
    profanity.load_censor_words()
    try:
        response = requests.get(url)
        response.raise_for_status()
        fact = response.json()
        fact_text = fact['fact'].replace("`", "\'")
        if profanity.contains_profanity(fact_text):
            print(f"Inappropriate fact: {fact_text}")
            return get_randomcatfact()
        else:
            return fact_text
    except requests.exceptions.RequestException as e:
        print(f'Can\'t get random cat facts.\nError:`{e}`')
        return None

def get_randomdogfact():
    url = 'https://dog-api.kinduff.com/api/facts'
    profanity.load_censor_words()
    try:
        response = requests.get(url)
        response.raise_for_status()
        fact = response.json()
        fact_text = fact['facts'][0].replace("`", "º")
        if profanity.contains_profanity(fact_text):
            print(f"Inappropriate fact: {fact_text}")
            return get_randomdogfact()
        else:
            return fact_text
    except requests.exceptions.RequestException as e:
        print(f'Can\'t get random dog facts.\nError:`{e}`')
        return None

def get_islandfact():
    with open(island_fact_database_path, encoding= "utf8") as f:
        json_content = json.load(f)

    random_key = random.choice(list(json_content.keys()))

    random_value = json_content[random_key]

    fact_object = {
        "Fact": random_value["fact"],
        "Image Link": random_value["img_link"],
        "Source Link": random_value["source_link"]
    }

    return fact_object

async def get_daily_islandfact():
    with open(island_fact_database_path, encoding= "utf8") as f:
        json_content = json.load(f)

    available_keys = [key for key, value in json_content.items() if not value["daily"]]

    while True:
        random_key = random.choice(available_keys)
        if not json_content[random_key]["daily"]:
            break

    random_value = json_content[random_key]

    json_content[random_key]["daily"] = True

    with open(island_fact_database_path, 'w', encoding="utf8") as f:
        json.dump(json_content, f, indent=4)

    fact_object = {
        "Fact": random_value["fact"],
        "Image Link": random_value["img_link"],
        "Source Link": random_value["source_link"]
    }


    # Update Github
    version_prefix = "**Version: "
    version_suffix = "**"
    
    with open(facts_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # get version
    version_line = next((line for line in lines if line.startswith(version_prefix)), None)
    if version_line is None:
        print(f"No line starts with '{version_prefix}'")
    else:
        version_index = lines.index(version_line)
        version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))

        version += 1

        # Update version
        lines[version_index] = version_prefix + str(version) + version_suffix + "\n"

        with open(facts_md_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    push_facts_github('./', [facts_md_path, added_trivia_path, island_fact_database_path, daily_count_path], f'[BOT] Update after send daily facy', 'kor', 'https://github.com/Stageddat/kor', token)
    return fact_object

def count_daily_status():
    with open(island_fact_database_path, encoding= "utf8") as f:
        json_content = json.load(f)

    true_count = 0
    false_count = 0

    for key, value in json_content.items():
        if value["daily"]:
            true_count += 1
        else:
            false_count += 1

    return {"True": true_count, "False": false_count}
