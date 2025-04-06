import pandas as pd
from typing import List
import os
import config

from parsing_old_employee import run_all_parsers
from prepare_data import (
    prepare_initial_data,
    DEFAULT_EXCLUDE_ROLES,
    DEFAULT_INPUT_FILES,
    save_dataframe
)
from llm_file import (
    process_profiles_with_llm,
    process_company_names
)
from more_requests import (
    process_profiles,
    filter_stealth_companies
)

def main():
    """
    Основная функция, выполняющая весь процесс анализа
    """
    # 0. Получение данных через API LinkedIn
    print("0. Получение данных через API LinkedIn...")
    run_all_parsers()
    print("Первичные данные получены и сохранены в CSV файлы")

    # 1. Подготовка данных
    print("\n1. Подготовка исходных данных...")
    filtered_df = prepare_initial_data(
        input_files=DEFAULT_INPUT_FILES,
        exclude_roles=DEFAULT_EXCLUDE_ROLES
    )
    save_dataframe(filtered_df, 'filtered_df.csv')
    print(f"Сохранено {len(filtered_df)} профилей в filtered_df.csv")

    # 2. Анализ с помощью LLM
    print("\n2. Анализ профилей с помощью LLM...")
    df_with_llm = process_profiles_with_llm(filtered_df, config.gpt_4o)
    save_dataframe(df_with_llm, 'profiles_with_llm.csv')
    print(f"Результаты LLM анализа сохранены в profiles_with_llm.csv")

    # 3. Классификация компаний
    print("\n3. Классификация названий компаний...")
    df_with_companies = process_company_names(df_with_llm, config.gpt_4o)
    
    # Фильтруем профили без текущей компании
    df_no_company = df_with_companies[df_with_companies['has_current_company'] == False]
    save_dataframe(df_no_company, 'profiles_without_company.csv')
    print(f"Найдено {len(df_no_company)} профилей без текущей компании")

    # 4. Запросы к API для получения деталей
    print("\n4. Получение деталей профилей через API...")
    df_with_details = process_profiles(df_no_company)
    save_dataframe(df_with_details, 'profiles_with_details.csv')
    print(f"Получены детали для {len(df_with_details)} профилей")

    # 5. Фильтрация stealth компаний
    print("\n5. Поиск stealth компаний...")
    df_stealth = filter_stealth_companies(df_with_details)
    save_dataframe(df_stealth, 'founders_in_stealth_companies.csv')
    print(f"Найдено {len(df_stealth)} профилей в stealth компаниях")

if __name__ == "__main__":
    main()
