from openai import OpenAI
from typing import Dict, Any
import json
import config
import pandas as pd
from tqdm import tqdm

client = OpenAI(api_key=config.OPENAI_API_KEY)

def llm_classifier(sub_title: str, skills: str, model: str) -> Dict[str, Any]:
    """
    Классифицирует профиль на основе заголовка и навыков
    
    Args:
        sub_title: Заголовок профиля
        skills: Навыки
        model: Модель OpenAI для использования
        
    Returns:
        Dict с результатами классификации
    """
    prompt = f"""
                Analyze the LinkedIn profile data to detect stealth startups and founder roles. 

                **1. Stealth Startup Indicators**

                a. Direct Evidence (any single mention is enough for `is_stealth = true`):
                    - The word "stealth" (case-insensitive) in the title (e.g., "Stealth Mode," "Stealth Startup")
                    - Terms like "undisclosed," "pre-launch," "unannounced," "confidential," "secret project"
                    - Phrases such as "in stealth" or "in stealth mode"

                b. Indirect Evidence (requires two or more of these signs to set `is_stealth = true`):
                    - No mention of a specific company or organization name (e.g., "Working on AI project" with no company name)
                    - Vague/placeholder descriptions like "New Venture," "Project X," **"Building something new," "building the future,"** 
                        "TBA/TBD project," "stay tuned," "unannounced product," or any synonyms that imply a mysterious or unrevealed project
                    - Very general claims with no real details (e.g., "Building something revolutionary," "Working on a big idea," 
                        "Something exciting coming soon," etc.)
                    - References to "hot" technologies (AI, Blockchain, Web3, Crypto, Quantum, etc.) **without** any concrete context 
                        or company details (indicating a possible stealth R&D effort)

                > **Note**: The model should interpret synonyms of these phrases that indicate a new or not-yet-disclosed project 
                > as potential stealth signals (e.g., "creating the future," "developing something undisclosed," 
                > "launching soon," etc.).

                **2. Founder Role Indicators** 
                - The following **explicit** words/phrases in the title → `is_founder = true`:
                    - "Founder," "Co-founder," "Owner"
                    - "Founding [Role]" (e.g., "Founding Engineer")
                    - References like "Built from scratch," "0 to 1," "my startup"
                - Exclusions (do not count as founder):
                    - "Ex-founder," "Former founder"
                    - "Advisor to startups," "Startup consultant," etc. (an advisory or third-party role, not an active founding member)

                **3. Input Data**:
                - `Current Position`: {sub_title}
                - `Skills`: {skills}

                **4. Output**:
                Return a concise JSON with the following structure:
                ```json
                {{
                    "is_stealth": true or false,
                    "is_founder": true or false,
                    "reason": "short explanation, e.g. 'Stealth in title' or 'No company + vague project'"
                }}
                ```
            """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Analyze LinkedIn profiles to identify stealth startups and founder roles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100,
            response_format={"type": "json_object"}  
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Ошибка при запросе к OpenAI: {e}")
        return {
            "is_stealth": False,
            "is_founder": False,
            "reason": "API Error"
        }

def company_name_classifier(sub_title: str, model: str) -> Dict[str, Any]:
    """
    Определяет, содержит ли заголовок профиля текущее название компании
    
    Args:
        sub_title: Заголовок профиля
        model: Модель OpenAI для использования
        
    Returns:
        Dict с результатами классификации
    """
    prompt = f"""
                Analyze the LinkedIn profile title and determine if it contains a CURRENT company name (True/False).

                Rules for identifying current company names:
                1. Company name should be a specific organization name, not an industry or activity description
                2. Current company names often appear after "@", "at", "in", or similar prepositions
                3. If all companies are prefixed with "ex-", "former", or similar, then there is no current company
                4. Generic descriptions like "stealth", "new venture", "something new", "crypto project" are NOT company names
                5. The company name should be for current employment (not past)

                Examples:

                FALSE cases (no current company mentioned):
                - "Building something new | ex-Google" (only past company)
                - "Something new coming soon" (no company name)
                - "Building something new | ex-Revolut, Lyft, YC S20" (only past companies)
                - "Building something new | Z-Fellow | ex-Yahoo, ex-Revolut" (no current company)
                - "Something New in Crypto (Ex.Revolut, Goldman Sachs)" (industry mention, not company name)
                - "Founder & CEO of Stealth Startup" (generic, not a specific company)
                - "Building the future of fintech" (activity description, not company)
                - "Entrepreneur in Residence" (role without company)

                TRUE cases (current company mentioned):
                - "Senior Product Manager @ KOMI | ex-Spotify & Revolut" (KOMI is current)
                - "Chief of Staff @ Simple App | ex-Revolut" (Simple App is current)
                - "Engineering Lead at Monzo Bank" (Monzo Bank is current)
                - "Product Manager @ N26 | Previously Revolut" (N26 is current)
                - "CEO of TechCorp | ex-Google" (TechCorp is current)

                Input title: "{sub_title}"

                Return JSON format:
                {{
                    "has_current_company": boolean,
                    "reason": "explanation of decision in 5-6 words"
                }}
                """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Analyze LinkedIn profiles to identify is there current company name or not."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100,
            response_format={"type": "json_object"}  
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Ошибка при запросе к OpenAI: {e}")
        return {
            "has_current_company": False,
            "reason": "API Error"
        }

def process_profiles_with_llm(df: pd.DataFrame, model: str) -> pd.DataFrame:
    """
    Обрабатывает профили с помощью LLM классификатора
    
    Args:
        df: DataFrame с профилями
        model: Модель OpenAI для использования
        
    Returns:
        pd.DataFrame: Обработанный DataFrame с результатами классификации
    """
    df['is_stealth'] = False
    df['is_founder'] = False
    df['stealth_reason'] = ""
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Анализ профилей"):
        try:
            result = llm_classifier(row['sub_title'], row.get('skills', ''), model)
            df.at[idx, 'is_stealth'] = result['is_stealth']
            df.at[idx, 'is_founder'] = result['is_founder']
            df.at[idx, 'stealth_reason'] = result['reason']
        except Exception as e:
            print(f"Ошибка при обработке строки {idx}: {e}")
            
    return df

def process_company_names(df: pd.DataFrame, model: str) -> pd.DataFrame:
    """
    Определяет наличие текущей компании в заголовках профилей
    
    Args:
        df: DataFrame с профилями
        model: Модель OpenAI для использования
        
    Returns:
        pd.DataFrame: Обработанный DataFrame с результатами классификации
    """
    df['has_current_company'] = False
    df['current_company_reason'] = ""
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Анализ профилей"):
        try:
            result = company_name_classifier(row['sub_title'], model)
            df.at[idx, 'has_current_company'] = result['has_current_company']
            df.at[idx, 'current_company_reason'] = result['reason']
        except Exception as e:
            print(f"Ошибка при обработке строки {idx}: {e}")
            
    return df
