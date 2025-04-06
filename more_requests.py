import requests
import json
import pandas as pd
from typing import Dict, Any, Optional
from tqdm import tqdm
import time
import os
import config

def format_date(date_dict: Dict) -> Optional[str]:
    """
    Форматирует словарь с датой в строку формата YYYY-MM
    
    Args:
        date_dict: Словарь с датой
        
    Returns:
        str: Отформатированная дата или None
    """
    if not date_dict or not date_dict.get('year'):
        return None
    
    month = str(date_dict.get('month', 1)).zfill(2)
    year = str(date_dict['year'])
    return f"{year}-{month}"

def extract_profile_info(json_data: Dict) -> Dict[str, Any]:
    """
    Извлекает информацию из JSON ответа API
    
    Args:
        json_data: JSON данные профиля
        
    Returns:
        Dict с извлеченной информацией
    """
    try:
        profile_info = {
            'api_sub_title': json_data['sub_title'],
            'current_position': None
        }
        
        if 'position_groups' in json_data and json_data['position_groups']:
            current_group = json_data['position_groups'][0]
            if current_group['profile_positions']:
                current_position = current_group['profile_positions'][0]
                profile_info['current_position'] = {
                    'company': current_group['company']['name'],
                    'title': current_position['title'],
                    'start_date': format_date(current_position['date']['start']),
                    'employment_type': current_position['employment_type'],
                    'location': current_position.get('location', 'N/A')
                }
        
        return profile_info
    
    except Exception as e:
        print(f"Ошибка при обработке данных: {str(e)}")
        return None

def get_profile_details(profile_id: str, api_key: str) -> Dict:
    """
    Получает детальную информацию о профиле через API
    
    Args:
        profile_id: ID профиля LinkedIn
        api_key: Ключ API
        
    Returns:
        Dict с ответом API
    """
    url = "https://api.proapis.com/iscraper/v4/profile-details"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    payload = {"profile_id": profile_id}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API вернул код {response.status_code}")

def process_profiles(df_input: pd.DataFrame, output_dir: str = 'final_request_to_api') -> pd.DataFrame:
    """
    Обрабатывает профили через API и сохраняет результаты
    
    Args:
        df_input: DataFrame с профилями
        output_dir: Директория для сохранения результатов
        
    Returns:
        pd.DataFrame: Обработанный DataFrame
    """
    os.makedirs(output_dir, exist_ok=True)
    new_data = []
    
    for _, row in tqdm(df_input.iterrows(), total=len(df_input), desc="Обработка профилей"):
        try:
            json_data = get_profile_details(row['profile_id'], config.PRO_API_KEY)
            
            # Сохраняем ответ API
            json_file_path = f"{output_dir}/{row['profile_id']}.json"
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            
            profile_info = extract_profile_info(json_data)
            
            if profile_info:
                profile_data = {
                    'profile_id': row['profile_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'linkedin_sub_title': row['sub_title'],
                    'li_url': row['li_url'],
                    'api_sub_title': profile_info['api_sub_title']
                }
                
                if profile_info['current_position']:
                    current = profile_info['current_position']
                    profile_data.update({
                        'current_company': current['company'],
                        'current_title': current['title'],
                        'start_date': current['start_date'],
                        'employment_type': current['employment_type'],
                        'location': current['location']
                    })
                else:
                    profile_data.update({
                        'current_company': None,
                        'current_title': None,
                        'start_date': None,
                        'employment_type': None,
                        'location': None
                    })
                
                new_data.append(profile_data)
        
        except Exception as e:
            print(f"Ошибка при обработке профиля {row['profile_id']}: {str(e)}")
        
        time.sleep(1)  # Задержка между запросами
    
    return pd.DataFrame(new_data)

def filter_stealth_companies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Фильтрует DataFrame, оставляя только профили со stealth компаниями
    
    Args:
        df: DataFrame с профилями
        
    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    rows_to_add = []
    
    for idx, row in df.iterrows():
        try:
            if pd.notna(row['current_company']) and 'stealth' in str(row['current_company']).lower():
                rows_to_add.append(row)
        except Exception as e:
            print(f"Ошибка при обработке строки {idx}: {e}")
    
    return pd.DataFrame(rows_to_add)
