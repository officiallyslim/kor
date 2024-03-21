import re
import json
from config import facts_md_path, island_fact_database_path, added_trivia_path
from src.facts.push_facts_github import push_facts_github

def sync_database():
    # Cargar el archivo Markdown
    with open(facts_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Extraer los hechos del archivo Markdown
    facts_pattern = re.compile(r"^(\d+)\.\s*(.+)$", re.MULTILINE)
    md_facts = {int(idx): fact.strip() for idx, fact in facts_pattern.findall(md_content)}

    # Cargar el archivo JSON existente
    with open(island_fact_database_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Sincronizar los hechos del Markdown con el JSON
    for fact_id, fact_text in md_facts.items():
        json_data[str(fact_id)] = {"fact": fact_text, "daily": json_data.get(str(fact_id), {}).get("daily", False), "img_link": json_data.get(str(fact_id), {}).get("img_link", None), "source_link": json_data.get(str(fact_id), {}).get("source_link", None)}

    # Eliminar los hechos del JSON que no están en el Markdown
    json_fact_ids = set(json_data.keys())
    md_fact_ids = set(str(idx) for idx in md_facts.keys())
    removed_facts = json_fact_ids - md_fact_ids
    for fact_id in removed_facts:
        del json_data[fact_id]

    # Guardar el JSON actualizado
    with open(island_fact_database_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    push_facts_github('./', [facts_md_path, added_trivia_path, island_fact_database_path], f'Sync facts', 'kor', 'https://github.com/Stageddat/kor')
    return True