import config
import requests
import json
import time
import csv
from pathlib import Path

def search_stealth_companies():
    url = "https://api.proapis.com/iscraper/v4/search/hosted/companies"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    # Используем Lucene синтаксис для поиска:
    # 1. Ищем компании со словом "stealth" в названии
    # 2. Фильтруем по количеству подписчиков (больше 50000)
    payload = {
        "page": 1,
        "per_page": 20,  # Увеличиваем количество результатов на страницу
        "query": '(name:*stealth* OR name:"stealth startup") AND followers:{50000 TO *}'
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # Создаем директорию companies, если она не существует
    companies_dir = Path("companies")
    companies_dir.mkdir(exist_ok=True)
    
    # Сохраняем результаты в JSON файл
    output_file = companies_dir / "stealth_companies_50k_plus.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)
    
    # Выводим краткую информацию о найденных компаниях
    data = response.json()
    if 'hits' in data:
        print(f"Найдено компаний: {data.get('total', 0)}")
        for company in data['hits']:
            print(f"\nНазвание: {company.get('name')}")
            print(f"Подписчиков: {company.get('followers', 'Н/Д')}")
            print(f"ID: {company.get('id')}")
    
    return response.json()

if __name__ == "__main__":
    search_stealth_companies()