import csv
import re

def analyze_potential_founders(csv_file_path):
    """
    Анализирует CSV-файл с данными о бывших сотрудниках Revolut
    и выявляет потенциальных основателей стелс-стартапов.
    
    Args:
        csv_file_path (str): Путь к CSV-файлу с данными профилей
    
    Returns:
        list: Список потенциальных основателей стелс-стартапов
    """
    # Ключевые слова-индикаторы основателя - расширенный список
    founder_keywords = [
        'founder', 'co-founder', 'ceo', 'chief executive', 'head', 'director', 'chairman'
    ]
    
    # Ключевые слова-индикаторы стелс-стартапа - расширенный список
    stealth_keywords = [
        'stealth', 'building', 'something new', 'coming soon', 
        'in development', 'new venture', 'working on', 'secret',
        'early stage', 'pre-launch', 'building something', 'new project',
        'undisclosed', 'confidential', 'in stealth', 'working on something',
        'metamorphosing', 'heads down', 'new in', 'learning and building',
        'next big thing', 'new chapter', 'stay tuned', 'watch this space'
    ]
    
    # Названия компаний, которые могут быть упомянуты, но не исключают стелс-режим
    # (часто упоминаются как предыдущие места работы)
    allowed_company_references = [
        'ex-', 'former', 'previously at', 'alumni', 'alum'
    ]
    
    # Паттерны, которые явно указывают на традиционную работу в компании (не стелс)
    exclude_patterns = [
        r'@ ([A-Za-z]|\.)+(\s+[A-Za-z]+){0,2}(?!\s*ex-|\s*former|\s*alumni|\s*alum|\s*previously)',  # работает в компании, но не "ex-"
        r'at ([A-Za-z]|\.)+(\s+[A-Za-z]+){0,2}(?!\s*ex-|\s*former|\s*alumni|\s*alum|\s*previously)',  # работает в компании, но не "ex-"
        r'building .* at',  # строит что-то в конкретной компании
    ]
    
    # Паттерны, которые повышают вероятность стелс-стартапа
    boost_patterns = [
        r'yc\s+[ws]\d+',  # YC W20, YC S21 и т.д. (Y Combinator)
        r'y\s*combinator',  # Y Combinator
        r'angel', # Angel, Angel Investor
        r'heads down',  # "Heads down" часто означает интенсивную работу над стартапом
        r'coming soon',
        r'payment',  # Связь с платежной индустрией (как Revolut)
        r'crypto',  # Криптовалюты - горячая область для стартапов
        r'web3',  # Web3 - горячая область для стартапов
        r'fintech',  # Финтех - горячая область для стартапов, связанная с Revolut
    ]
    
    # Индустрии, связанные с созданием стартапов бывшими сотрудниками Revolut
    relevant_industries = [
        'payments', 'fintech', 'finance', 'banking', 'crypto', 'blockchain', 'web3',
        'ai', 'artificial intelligence', 'machine learning', 'data science',
        'cybersecurity', 'security'
    ]
    
    potential_founders = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for profile in reader:
            is_founder = False
            is_stealth = False
            stealth_indicators = []
            founder_indicators = []
            bonus_indicators = []
            
            sub_title = profile.get('sub_title', '').lower()
            
            # Проверка на признаки основателя
            for keyword in founder_keywords:
                if keyword in sub_title:
                    # Проверяем, что это не "Head of [Department]" или "Director of [Department]"
                    if keyword in ['head', 'director'] and re.search(rf'{keyword} of', sub_title, re.IGNORECASE):
                        continue
                    
                    is_founder = True
                    founder_indicators.append(keyword)
            
            # Проверяем, что не указана конкретная компания (кроме разрешенных упоминаний)
            excluded = False
            for pattern in exclude_patterns:
                if re.search(pattern, sub_title, re.IGNORECASE):
                    # Проверяем, нет ли разрешенных упоминаний компаний
                    skip_exclusion = False
                    for allowed_ref in allowed_company_references:
                        if allowed_ref in sub_title.lower():
                            skip_exclusion = True
                            break
                    
                    if not skip_exclusion:
                        excluded = True
                        break
            
            # Проверка на признаки стелс-стартапа
            for keyword in stealth_keywords:
                if keyword in sub_title:
                    is_stealth = True
                    stealth_indicators.append(keyword)
            
            # Проверка на повышающие вероятность паттерны
            for pattern in boost_patterns:
                if re.search(pattern, sub_title, re.IGNORECASE):
                    is_stealth = True
                    bonus_indicators.append(pattern)
            
            # Проверка на релевантные индустрии
            for industry in relevant_industries:
                if industry in sub_title:
                    bonus_indicators.append(industry)
            
            # Если человек основатель, но не указал название компании - это может быть стелс
            if is_founder and not excluded:
                # Ищем явное название компании
                company_name_found = re.search(r'(ceo|founder|co-founder) (?:of|at) ([A-Za-z]+)', sub_title, re.IGNORECASE)
                
                if company_name_found:
                    # Исключаем если есть конкретная компания, но добавляем её в список
                    company_name = company_name_found.group(2)
                    bonus_indicators.append(f'company_name: {company_name}')
                else:
                    is_stealth = True
                    stealth_indicators.append('no_company_name')
            
            # Определяем уровень уверенности
            confidence = 'Низкая'
            if is_founder and is_stealth:
                confidence = 'Высокая'
            elif is_founder or (is_stealth and len(stealth_indicators) > 1):
                confidence = 'Средняя'
            elif len(bonus_indicators) >= 2:
                confidence = 'Средняя'
            
            # Если профиль соответствует хотя бы одному из признаков стелс-стартапа
            if is_stealth or (is_founder and not excluded) or len(bonus_indicators) >= 2:
                
                founder_info = {
                    'profile_id': profile.get('profile_id', ''),
                    'name': f"{profile.get('first_name', '')} {profile.get('last_name', '')}",
                    'sub_title': profile.get('sub_title', ''),
                    'location': f"{profile.get('location_city', '')}, {profile.get('location_country', '')}",
                    'linkedin_url': profile.get('li_url', ''),
                    'is_founder': is_founder,
                    'is_stealth': is_stealth,
                    'founder_indicators': founder_indicators,
                    'stealth_indicators': stealth_indicators,
                    'bonus_indicators': bonus_indicators,
                    'confidence': confidence
                }
                
                potential_founders.append(founder_info)
    
    # Сортировка по уровню уверенности
    confidence_order = {'Высокая': 0, 'Средняя': 1, 'Низкая': 2}
    potential_founders.sort(key=lambda x: confidence_order[x['confidence']])
    
    return potential_founders

def save_potential_founders_csv(potential_founders, output_file_path):
    """
    Сохраняет список потенциальных основателей в CSV-файл
    
    Args:
        potential_founders (list): Список потенциальных основателей
        output_file_path (str): Путь для сохранения выходного CSV-файла
    """
    if not potential_founders:
        print("Нет потенциальных основателей для сохранения.")
        return
    
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'profile_id', 'name', 'sub_title', 'location', 'linkedin_url',
            'is_founder', 'is_stealth', 'founder_indicators', 'stealth_indicators', 
            'bonus_indicators', 'confidence'
        ]
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for founder in potential_founders:
            # Преобразование списков в строки для CSV
            founder_copy = founder.copy()
            founder_copy['founder_indicators'] = ', '.join(founder_copy['founder_indicators'])
            founder_copy['stealth_indicators'] = ', '.join(founder_copy['stealth_indicators'])
            founder_copy['bonus_indicators'] = ', '.join(founder_copy['bonus_indicators'])
            
            writer.writerow(founder_copy)
    
    print(f"Список потенциальных основателей сохранен в {output_file_path}")

def print_founders_summary(potential_founders):
    """
    Выводит сводку о найденных потенциальных основателях
    
    Args:
        potential_founders (list): Список потенциальных основателей
    """
    if not potential_founders:
        print("Потенциальных основателей не найдено.")
        return
    
    print(f"\nНайдено {len(potential_founders)} потенциальных основателей стелс-стартапов:")
    
    # Статистика по уровням уверенности
    confidence_levels = {}
    for founder in potential_founders:
        confidence = founder['confidence']
        confidence_levels[confidence] = confidence_levels.get(confidence, 0) + 1
    
    for level, count in sorted(confidence_levels.items(), key=lambda x: ['Высокая', 'Средняя', 'Низкая'].index(x[0])):
        print(f"- {level} уверенность: {count} профилей")
    
    # Топ-5 профилей с высокой уверенностью
    high_confidence = [f for f in potential_founders if f['confidence'] == 'Высокая']
    if high_confidence:
        print("\nТоп-5 профилей с высокой уверенностью:")
        for i, founder in enumerate(high_confidence[:5], 1):
            print(f"{i}. {founder['name']}: {founder['sub_title']}")
            print(f"   LinkedIn: {founder['linkedin_url']}")
    
    # Топ-5 профилей со средней уверенностью
    medium_confidence = [f for f in potential_founders if f['confidence'] == 'Средняя']
    if medium_confidence:
        print("\nТоп-5 профилей со средней уверенностью:")
        for i, founder in enumerate(medium_confidence[:5], 1):
            print(f"{i}. {founder['name']}: {founder['sub_title']}")
            print(f"   LinkedIn: {founder['linkedin_url']}")
    
    print("\nРезультаты сохранены в CSV-файле для дальнейшего анализа.")

if __name__ == "__main__":
    input_file = "revolut_employees_20250402_220231.csv"
    output_file = "potential_founders_stealth_improved.csv"
    
    print("Анализ профилей бывших сотрудников Revolut на предмет основателей стелс-стартапов...")
    
    potential_founders = analyze_potential_founders(input_file)
    save_potential_founders_csv(potential_founders, output_file)
    print_founders_summary(potential_founders)
