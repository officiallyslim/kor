import json
from src.global_src.global_path import bss_codes_path
from bs4 import BeautifulSoup
import requests

def load_codes():
    try:
        with open(bss_codes_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def check_codes(new_codes, current_codes):
    # set news
    news = set(new_codes.keys()) - set(current_codes.keys())
    invalid = set(current_codes.keys()) - set(new_codes.keys())
    common = set(new_codes.keys()) & set(current_codes.keys())

    # set none if empty
    news = None if not news else news
    invalid = None if not invalid else invalid
    common = None if not common else common

    print(f"Códigos nuevos: {news}")
    print(f"Códigos eliminados: {invalid}")
    print(f"Códigos comunes: {common}")

    return news, invalid, common


async def scrap_wiki():
    url = "https://bee-swarm-simulator.fandom.com/wiki/Codes"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        valid_codes_table = soup.find("table", {"class": "article-table sortable"})
        
        if valid_codes_table:
            rows = valid_codes_table.find("tbody").find_all("tr")[1:]
            
            codes_data = {}
            
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 4:
                    code = cells[0].get_text(strip=True)
                    location = cells[1].get_text(strip=True)
                    added_date = cells[2].get_text(strip=True)
                    reward = cells[3].get_text(strip=True)
                    
                    codes_data[code] = {
                        "location": location,
                        "added_date": added_date,
                        "reward": reward
                    }

            current_codes = load_codes()

            with open(bss_codes_path, "w", encoding="utf-8") as file:
                json.dump(codes_data, file, ensure_ascii=False, indent=4)

            news, invalid, common = check_codes(codes_data, current_codes)
            return news, invalid, common
        else:
            return("No table found")
    else:
        return(f"Failed: {response.status_code}")
