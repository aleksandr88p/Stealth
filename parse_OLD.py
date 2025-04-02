import config
import requests
import json
import time

def search_revolut_employees_first_page():
    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "page": 1,
        "per_page": 20,  # Максимум 20
        "query": "past_companies:5356541"
    }
    
    # Делаем запрос
    response = requests.post(url, headers=headers, json=payload)
    
    # Проверяем статус ответа
    if response.status_code == 200:
        data = response.json()
        print("Данные успешно получены:")
        print(data)
        
        # Сохраняем ответ в файл
        with open('revolut_employees_first_page.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")

# Вызываем функцию
search_revolut_employees_first_page()