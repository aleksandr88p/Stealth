# Stealth Startup Founder Finder 🔍
[English](#english) | [Русский](#русский)

<a name="english"></a>
## 🌍 English

### Overview
A tool for identifying founders of stealth startups among former employees of specific companies (e.g., Revolut) using LinkedIn data through ProApis LinkedIn API and OpenAI GPT-4.

### Features
- 🤖 AI-powered profile analysis
- 💾 Efficient data caching
- 🔄 Multi-stage filtering process
- 📊 Structured data output
- 🔍 Smart search algorithms

### Requirements
- Python 3.11+
- OpenAI API key
- ProApis LinkedIn API key

### Setup
1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
PRO_API_KEY=your_proapis_linkedin_api_key
```

### Usage
Run the main script:
```bash
python main.py
```

### Process Steps
1. **Initial Data Collection** (Step 0)
   - Fetches data via LinkedIn API
   - Output: `revolut_past_key_roles.csv`, `revolut_current_founders.csv`, `revolut_stealth_indicators.csv`

2. **Data Preparation** (Step 1)
   - Combines and filters profiles
   - Output: `filtered_df.csv`

3. **LLM Analysis** (Step 2)
   - Analyzes profiles using GPT-4
   - Output: `profiles_with_llm.csv`

4. **Company Classification** (Step 3)
   - Identifies current companies
   - Output: `profiles_without_company.csv`

5. **Profile Details** (Step 4)
   - Fetches detailed profile information
   - Output: `profiles_with_details.csv`

6. **Stealth Company Detection** (Step 5)
   - Final filtering of stealth startups
   - Output: `founders_in_stealth_companies.csv`

### APIs Used
- **ProApis LinkedIn API**: For fetching LinkedIn profiles and company data
- **OpenAI GPT-4**: For intelligent profile analysis and classification

---

<a name="русский"></a>
## 🌍 Русский

### Обзор
Инструмент для поиска основателей stealth-стартапов среди бывших сотрудников определенных компаний (например, Revolut) с использованием данных LinkedIn через ProApis LinkedIn API и OpenAI GPT-4.

### Возможности
- 🤖 Анализ профилей с помощью ИИ
- 💾 Эффективное кэширование данных
- 🔄 Многоступенчатая фильтрация
- 📊 Структурированный вывод данных
- 🔍 Умные алгоритмы поиска

### Требования
- Python 3.11+
- Ключ API OpenAI
- Ключ API ProApis LinkedIn

### Установка
1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории:
```env
OPENAI_API_KEY=ваш_ключ_openai_api
PRO_API_KEY=ваш_ключ_proapis_linkedin_api
```

### Использование
Запустите основной скрипт:
```bash
python main.py
```

### Этапы Процесса
1. **Сбор Исходных Данных** (Шаг 0)
   - Получение данных через LinkedIn API
   - Результат: `revolut_past_key_roles.csv`, `revolut_current_founders.csv`, `revolut_stealth_indicators.csv`

2. **Подготовка Данных** (Шаг 1)
   - Объединение и фильтрация профилей
   - Результат: `filtered_df.csv`

3. **LLM Анализ** (Шаг 2)
   - Анализ профилей с помощью GPT-4
   - Результат: `profiles_with_llm.csv`

4. **Классификация Компаний** (Шаг 3)
   - Определение текущих компаний
   - Результат: `profiles_without_company.csv`

5. **Детали Профилей** (Шаг 4)
   - Получение подробной информации о профилях
   - Результат: `profiles_with_details.csv`

6. **Обнаружение Stealth-компаний** (Шаг 5)
   - Финальная фильтрация stealth-стартапов
   - Результат: `founders_in_stealth_companies.csv`

### Используемые API
- **ProApis LinkedIn API**: Для получения данных о профилях и компаниях LinkedIn
- **OpenAI GPT-4**: Для интеллектуального анализа и классификации профилей 