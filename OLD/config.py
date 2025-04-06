import os
import dotenv

dotenv.load_dotenv()

PRO_API_KEY = os.getenv("PRO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

o3_mini = 'o3-mini-2025-01-31'
gpt_4o = 'gpt-4o-2024-08-06'