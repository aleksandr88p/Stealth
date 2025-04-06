import pandas as pd
from typing import List, Dict, Any
import os

def combine_csv_files(csv_files: List[str]) -> pd.DataFrame:
    """
    Объединяет несколько CSV файлов в один DataFrame
    
    Args:
        csv_files: Список путей к CSV файлам
        
    Returns:
        pd.DataFrame: Объединенный DataFrame
    """
    combined_df = pd.DataFrame()
    
    for file in csv_files:
        df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    return combined_df

def remove_duplicates(df: pd.DataFrame, subset: str = 'profile_id') -> pd.DataFrame:
    """
    Удаляет дубликаты из DataFrame по указанному столбцу
    
    Args:
        df: Исходный DataFrame
        subset: Столбец для проверки дубликатов
        
    Returns:
        pd.DataFrame: DataFrame без дубликатов
    """
    return df.drop_duplicates(subset=subset)

def filter_roles(df: pd.DataFrame, exclude_roles: List[str]) -> pd.DataFrame:
    """
    Фильтрует DataFrame, исключая определенные роли
    
    Args:
        df: Исходный DataFrame
        exclude_roles: Список ролей для исключения
        
    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    exclude_pattern = '|'.join(exclude_roles)
    filtered_df = df[
        ~df['sub_title'].str.contains(exclude_pattern, case=False, na=False)
    ]
    return filtered_df

def prepare_initial_data(input_files: List[str], exclude_roles: List[str]) -> pd.DataFrame:
    """
    Основная функция для подготовки данных
    
    Args:
        input_files: Список входных CSV файлов
        exclude_roles: Список ролей для исключения
        
    Returns:
        pd.DataFrame: Обработанный DataFrame
    """
    # Объединяем файлы
    combined_df = combine_csv_files(input_files)
    
    # Удаляем дубликаты
    combined_df = remove_duplicates(combined_df)
    
    # Фильтруем роли
    filtered_df = filter_roles(combined_df, exclude_roles)
    
    return filtered_df

def save_dataframe(df: pd.DataFrame, output_file: str) -> None:
    """
    Сохраняет DataFrame в CSV файл
    
    Args:
        df: DataFrame для сохранения
        output_file: Путь к выходному файлу
    """
    df.to_csv(output_file, index=False)

# Константы
DEFAULT_EXCLUDE_ROLES = [" hr ", "recruiter", "accountant", "legal", "lawyer"]
DEFAULT_INPUT_FILES = [
    "revolut_past_key_roles.csv",
    "revolut_current_founders.csv",
    "revolut_stealth_indicators.csv"
]
