import config
import requests
import json
import time
import csv
import os

def search_company():
    url = "https://api.proapis.com/iscraper/v4/search/hosted/companies"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "page": 1,
        "per_page": 10,
        "query": "name:\"Stealth Startup\""
    }
    
    response = requests.post(url, headers=headers, json=payload)

    with open('stealth_company_data.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)
    
    return response.json()

def parse_revolut_by_past_roles():
    """
    Парсит бывших сотрудников Revolut по их прошлым должностям в компании
    """
    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    
    roles_query_parts = []
    for role in config.KEY_ROLES:
        roles_query_parts.append(f'past_job_titles:{role}')
    
    roles_query = " OR ".join(roles_query_parts)
    query = f"past_companies:5356541 AND ({roles_query})"
    

    print(f"DEBUG - Запрос к API: {query}")
    
    csv_filename = "revolut_past_key_roles.csv"
    json_folder = "past_roles_json"
    
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    

    _fetch_profiles(url, headers, query, csv_filename, "past_roles", json_folder)
    
    return csv_filename

def parse_revolut_founders():

    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    

    

    roles_query_parts = []
    for role in config.FOUNDER_ROLES:
        roles_query_parts.append(f'current_job_titles:{role}')
    
    roles_query = " OR ".join(roles_query_parts)
    query = f"past_companies:5356541 AND ({roles_query})"
    

    print(f"DEBUG - Запрос к API: {query}")
    
    csv_filename = "revolut_current_founders.csv"
    json_folder = "founders_json"
    

    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    

    _fetch_profiles(url, headers, query, csv_filename, "founder", json_folder)
    
    return csv_filename

def parse_revolut_stealth_titles():

    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    

    keywords_query_parts = []
    for keyword in config.STEALTH_KEYWORDS:

        if " " in keyword:
            keywords_query_parts.append(f'sub_title:"{keyword}"')
        else:
            keywords_query_parts.append(f'sub_title:{keyword}')
    
    keywords_query = " OR ".join(keywords_query_parts)
    query = f"past_companies:5356541 AND ({keywords_query})"
    
    
    print(f"DEBUG - Запрос к API: {query}")
    
    csv_filename = "revolut_stealth_indicators.csv"
    json_folder = "stealth_json"
    
    
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    
    
    _fetch_profiles(url, headers, query, csv_filename, "stealth_title", json_folder)
    
    return csv_filename

def _fetch_profiles(url, headers, query, csv_filename, query_type, json_folder):
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'profile_id', 'first_name', 'last_name', 'sub_title', 
            'location_city', 'location_country', 'li_url', 'skills',
            'query_type'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        profiles_fetched = 0
        page = 1
        has_more_pages = True
        
        while has_more_pages:
            print(f"Загрузка страницы {page} для запроса {query_type}...")
            
            payload = {
                "page": page,
                "per_page": 20,
                "query": query
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                
                api_response = response.json()
                
                json_path = os.path.join(json_folder, f'page_{page}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(api_response, f, ensure_ascii=False, indent=2)
                
                profiles = api_response.get('data', [])
                
                if not profiles:
                    print(f"Нет данных на странице {page}. Завершаем запрос.")
                    has_more_pages = False
                    continue
                
                for profile in profiles:
                    skills_str = ', '.join(profile.get('skills', [])) if profile.get('skills') else ''
                    
                    profile_data = {
                        'profile_id': profile.get('profile_id', ''),
                        'first_name': profile.get('first_name', ''),
                        'last_name': profile.get('last_name', ''),
                        'sub_title': profile.get('sub_title', ''),
                        'location_city': profile.get('location_city', ''),
                        'location_country': profile.get('location_country', ''),
                        'li_url': profile.get('li_url', ''),
                        'skills': skills_str,
                        'query_type': query_type
                    }
                    
                    writer.writerow(profile_data)
                    profiles_fetched += 1
                
                print(f"Получено {len(profiles)} профилей со страницы {page}. Всего: {profiles_fetched}")
                
                pagination = api_response.get('pagination', {})
                total_pages = pagination.get('total_pages', 0)
                
                if page >= total_pages:
                    has_more_pages = False
                else:
                    page += 1
                    time.sleep(1)
            
            except Exception as e:
                print(f"Ошибка при выполнении запроса: {e}")
                has_more_pages = False
    
    print(f"Парсинг завершен. Получено {profiles_fetched} профилей.")
    print(f"Данные сохранены в файл: {csv_filename}")
    print(f"JSON-файлы сохранены в папку: {json_folder}")


def parse_revolut_specific_companies():
    """
    Парсит бывших сотрудников Revolut, которые сейчас работают в конкретных компаниях
    """
    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    

    
    companies_query = " OR ".join(f"current_companies:{company_id}" for company_id in config.TARGET_COMPANIES)
    query = f"past_companies:5356541 AND ({companies_query})"
    
    print(f"DEBUG - Запрос к API: {query}")
    
    csv_filename = "revolut_specific_companies.csv"
    json_folder = "specific_companies_json"
    
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    
    _fetch_profiles(url, headers, query, csv_filename, "specific_companies", json_folder)
    
    return csv_filename

def run_all_parsers():
    """
    Запускает все три парсера последовательно
    """
    print("Запуск парсера по прошлым должностям...")
    parse_revolut_by_past_roles()
    
    print("\nЗапуск парсера по текущим должностям основателей...")
    parse_revolut_founders()
    
    print("\nЗапуск парсера по стелс-индикаторам в профилях...")
    parse_revolut_stealth_titles()

    print("\nЗапуск парсера по конкретным компаниям...")
    parse_revolut_specific_companies()
    
    print("\nВсе парсеры завершили работу!")


