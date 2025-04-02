import config
import requests
import csv
import time
import os
from datetime import datetime

def parse_revolut_employees(total_profiles=200):
    """
    Функция для парсинга бывших сотрудников Revolut через API.
    Парсит указанное количество профилей и сохраняет их в CSV файл.
    
    Args:
        total_profiles (int): Общее количество профилей для парсинга
    """
    url = "https://api.proapis.com/iscraper/v4/search/hosted/people"
    headers = {
        "x-api-key": config.PRO_API_KEY,
        "content-type": "application/json"
    }
    
    # Путь для сохранения CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"revolut_employees_{timestamp}.csv"
    
    # Параметры для пагинации
    per_page = 20  # Максимальное значение для API
    total_pages = (total_profiles + per_page - 1) // per_page  # Округление вверх
    
    # Счетчики для мониторинга прогресса
    profiles_fetched = 0
    
    # Создаем CSV файл и записываем заголовки
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'profile_id', 'first_name', 'last_name', 'sub_title', 
            'location_city', 'location_country', 'li_url', 'skills'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Цикл по страницам
        for page in range(1, total_pages + 1):
            print(f"Получение страницы {page} из {total_pages}...")
            
            payload = {
                "page": page,
                "per_page": per_page,
                "query": "past_companies:5356541"  # ID компании Revolut
            }
            
            # Отправляем запрос с повторными попытками в случае ошибки
            max_retries = 3
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    response.raise_for_status()  # Проверка на ошибки HTTP
                    success = True
                except Exception as e:
                    retry_count += 1
                    print(f"Ошибка при запросе ({retry_count}/{max_retries}): {e}")
                    if retry_count < max_retries:
                        time.sleep(2 * retry_count)  # Увеличиваем время ожидания с каждой попыткой
                    else:
                        print(f"Не удалось получить страницу {page} после {max_retries} попыток")
                        break
            
            if not success:
                continue
                
            # Обрабатываем успешный ответ
            data = response.json()
            
            # Проверяем, есть ли данные
            if not data.get('data'):
                print(f"Нет данных на странице {page}. Возможно, достигнут конец результатов.")
                break
                
            # Записываем профили в CSV
            for profile in data.get('data', []):
                # Обработка списка навыков
                skills_str = ', '.join(profile.get('skills', [])) if profile.get('skills') else ''
                
                # Создаем словарь профиля для CSV
                profile_data = {
                    'profile_id': profile.get('profile_id', ''),
                    'first_name': profile.get('first_name', ''),
                    'last_name': profile.get('last_name', ''),
                    'sub_title': profile.get('sub_title', ''),
                    'location_city': profile.get('location_city', ''),
                    'location_country': profile.get('location_country', ''),
                    'li_url': profile.get('li_url', ''),
                    'skills': skills_str
                }
                
                # Записываем профиль в CSV
                writer.writerow(profile_data)
                profiles_fetched += 1
            
            # Выводим прогресс
            print(f"Всего получено профилей: {profiles_fetched}")
            
            # Если достигли нужного количества профилей, останавливаемся
            if profiles_fetched >= total_profiles:
                break
                
            # Задержка перед следующим запросом для избежания ограничений API
            time.sleep(1)
    
    print(f"Парсинг завершен. Получено {profiles_fetched} профилей.")
    print(f"Данные сохранены в файл: {csv_filename}")
    return csv_filename

if __name__ == "__main__":
    print("Начинаем парсинг бывших сотрудников Revolut...")
    csv_file = parse_revolut_employees(200)  # Парсим 200 профилей (10 страниц по 20)
    print(f"Готово! Файл с данными: {csv_file}")