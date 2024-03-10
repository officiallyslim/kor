from better_profanity import profanity
import requests

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
        fact_text = fact['facts'][0].replace("`", "\'")
        if profanity.contains_profanity(fact_text):
            print(f"Inappropriate fact: {fact_text}")
            return get_randomdogfact()
        else:
            return fact_text
    except requests.exceptions.RequestException as e:
        print(f'Can\'t get random dog facts.\nError:`{e}`')
        return None
