import config
import requests
import json
import time

def search_revolut():
    url = "https://api.proapis.com/iscraper/v4/search/hosted/companies"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "page": 1,
        "per_page": 10,
        "query": "name:\"Revolut\""
    }
    
    response = requests.post(url, headers=headers, json=payload)

    with open('revolut_company_data.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)
    
    return response.json()

def search_revolut_employees():
    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    all_employees = []
    current_page = 1
    
    while True:
        payload = {
            "page": current_page,
            "per_page": 100,
            "query": "past_companies:5356541"
        }
        
        print(f"Получаем страницу {current_page}...")
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # Сохраняем промежуточные результаты
        with open(f'revolut_employees_page_{current_page}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if not data.get('data'):  # Если нет данных, значит достигли конца
            break
            
        all_employees.extend(data.get('data', []))
        print(f"Получено сотрудников: {len(all_employees)}")
        
        # Проверяем, есть ли еще страницы
        if current_page >= data.get('pagination', {}).get('total_pages', 1):
            break
            
        current_page += 1
        time.sleep(1)  # Задержка между запросами
    
    # Сохраняем все результаты
    with open('all_revolut_employees.json', 'w', encoding='utf-8') as f:
        json.dump({
            "total_employees": len(all_employees),
            "data": all_employees
        }, f, ensure_ascii=False, indent=2)
    
    return all_employees

# revolut_data = search_revolut()

# Вызываем функцию и получаем результат





