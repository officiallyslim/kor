import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from config import facts_md_path, island_base_url, added_trivia_path, island_fact_database_path
import json
from urllib.parse import urlparse, urlunparse
from datetime import datetime
import pytz
from git import Repo

async def extract_trivia(url, name):
    # Open URL
    url_search = urlopen(url)
    island_page = url_search.read()

    # Get HTML
    island_html = bs(island_page, "html.parser")

    # Search Trivia
    trivia_section = island_html.find('span', {'id': 'Trivia'}).parent if island_html.find('span', {'id': 'Trivia'}) else None

    if trivia_section:
        trivia_content = trivia_section.find_next_sibling('ul')
        if trivia_content:
            facts = extract_data(trivia_content, url)
            if facts != 404:
                added_numbers = add_to_md(facts, name)
                print(added_numbers)
                add_to_log(url)
                return facts, added_numbers
            else:
                add_to_log(url)
                return 404
        else:
            add_to_log(url)
            return "No trivia"
    else:
        add_to_log(url)
        return "No trivia"

def extract_data(html, page_url):
    soup = html
    data = []
    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        for a_tag in li.find_all("a"):
            url = island_base_url + a_tag.get("href")
            link_text = a_tag.get_text(strip=True)
            if text[text.find(link_text) + len(link_text):].startswith(('.', ',')):
                text = text.replace(link_text, f" [{link_text}]({url})")
            else:
                text = text.replace(link_text, f" [{link_text}]({url}) ")
        data.append(text)

    # Clear links
    new_data = []
    pattern = r'\s{2,}\[([^\]]+)\]\([^)]+\)'
    for item in data:
        new_item = re.sub(pattern, r' \1', item)
        new_item += ' '
        new_data.append(new_item)

        add_to_database(new_item, page_url)
    return new_data

def add_to_md(data, user):
    version_prefix = "**Version: "
    version_suffix = "**"
    updated_by_prefix = "**Updated by: "
    updated_at_prefix = "**Updated at: "
    
    with open(facts_md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # get version
    version_line = next((line for line in lines if line.startswith(version_prefix)), None)
    if version_line is None:
        print(f"No line starts with '{version_prefix}'")
        return

    version_index = lines.index(version_line)
    version = int(version_line.strip().replace(version_prefix, "").replace(version_suffix, ""))

    version += 1

    # Update version
    lines[version_index] = version_prefix + str(version) + version_suffix + "\n"

    # Update user
    updated_by_line = next((line for line in lines if line.startswith(updated_by_prefix)), None)
    if updated_by_line is not None:
        updated_by_index = lines.index(updated_by_line)
        lines[updated_by_index] = updated_by_prefix + user + version_suffix + "\n"

    # Update time
    updated_at_line = next((line for line in lines if line.startswith(updated_at_prefix)), None)
    if updated_at_line is not None:
        updated_at_index = lines.index(updated_at_line)
        est = pytz.timezone('US/Eastern')
        est_time = datetime.now(est).strftime('%H:%M EST')
        lines[updated_at_index] = updated_at_prefix + est_time + version_suffix + "\n"

    # get the last number
    last_number_line = next((line for line in reversed(lines) if line[0].isdigit()), None)
    if last_number_line is None:
        last_number = 0
    else:
        last_number = int(last_number_line.split()[0].replace('.', ''))

    added_numbers = []

    # add data
    for item in data:
        last_number += 1
        lines.append(str(last_number) + ". " + item + "\n")  # Add a period and a space after the number
        added_numbers.append(last_number)

    # save
    with open(facts_md_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return added_numbers

async def check_existing_link(link):
    # parse de link for get base
    parse_link = urlparse(link)
    base_link = urlunparse(parse_link._replace(fragment=''))

    # Load json
    with open(added_trivia_path, 'r') as file:
        links = json.load(file)

    # parse and check in the json file
    for link in links:
        parse_link = urlparse(link)
        link_base = urlunparse(parse_link._replace(fragment=''))
        if base_link == link_base:
            return True
    return False

async def check_link(link):
    # parse link
    parse_link = urlparse(link)
    parse_base = urlparse(island_base_url)

    # check
    return (parse_link.scheme == parse_base.scheme and
            parse_link.netloc == parse_base.netloc)

def add_to_database(fact, url):
    # load
    with open(island_fact_database_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # object it
    new_entry = {
        "fact": fact,
        "daily": False,
        "img_link": None,
        "source_link": url
    }
    # add
    next_index = str(int(max(data.keys(), key=int)) + 1)
    data[next_index] = new_entry

    # save
    with open(island_fact_database_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_to_log(url):
    with open(added_trivia_path, 'r', encoding='utf-8') as file:
        links_list = json.load(file)

    # Añadir el nuevo enlace a la lista
    links_list.append(url)

    # Guardar la lista actualizada en el archivo JSON
    with open(added_trivia_path, 'w', encoding='utf-8') as file:
        json.dump(links_list, file, ensure_ascii=False, indent=4)