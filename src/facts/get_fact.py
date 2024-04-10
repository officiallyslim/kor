import os

import dotenv
import requests
from better_profanity import profanity
from requests.exceptions import HTTPError

dotenv.load_dotenv()
private_api = str(os.getenv("PRIVATE_API"))
private_api_token = str(os.getenv("PRIVATE_API_KEY_TOKEN"))

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
    try:
        headers = {'Authorization': private_api_token}
        response = requests.get("http://144.76.143.198:8163/get_island_fact", headers=headers)
        response.raise_for_status()
        fact = response.json()

    except Exception as e:
        print("Failed get island fact on the private API", e)
        return

    fact_object = {
        "Fact": fact['Fact'],
        "Image Link": fact['Image Link'],
        "Source Link": fact['Source Link']
    }
    return fact_object

async def get_daily_islandfact():
    try:
        headers = {'Authorization': private_api_token}
        response = requests.get(f"{private_api}/get_daily_island_fact", headers=headers)
        response.raise_for_status()
        fact = response.json()

    except HTTPError as e:
        if e.response.status_code == 404:
            print("No fact avaible!")
            return None
        else:
            print(f"HTTP ERROR: {e}")

    except Exception:
        print("Failed get daily fact on the private API")

    if fact:
        fact_object = {
            "Fact": fact['Fact'],
            "Image Link": fact['Image Link'],
            "Source Link": fact['Source Link'],
            "Available Facts": fact['Available Facts']
        }
        return fact_object
    else:
        print("No fact avaible!")