from better_profanity import profanity
import requests
import random
import json
from config import island_fact_database_path

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
