import os
import dotenv

dotenv.load_dotenv()

PRO_API_KEY = os.getenv("PRO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

o3_mini = 'o3-mini-2025-01-31'
gpt_4o = 'gpt-4o-2024-08-06'

KEY_ROLES = [
        "head", "senior", "lead", "general", "chief", 
        "director", "vp", "manager", "executive", 
        "product", "strategy", "owner", "consultant", 
        "advisor", "account", "engineer", "developer", 
        "tech", "architect", "research", "data"
    ]


FOUNDER_ROLES = [
        "founder", "co-founder", "ceo", "chief", 
        "entrepreneur", "owner", 'cto'
    ]

STEALTH_KEYWORDS = [
        "stealth", "building", "new venture", 
        "startup", "new company", "secretive",
        'something', 'thing', 'other', 'pre-product', 'pre-revenue', 'pre-launch', '0 to 1', 'incubation', 
        "undisclosed", "confidential", "unannounced", "unrevealed", "hidden", "pre-seed",
        "working on", "co-founding", "building quietly", "under the radar", 
        "heads down", "secret project", "early stage", "early venture", "tbd", 
        "next thing", "not public", "0→1", "zero to one", "private company", 
        "stealth mode", "non-public", "incubating", "exploring", "in stealth", 
        "coming soon", "soft launch", "low profile", "covert", "redacted"
    ]   

# ID компаний (stealth)
TARGET_COMPANIES = [18583501, 18016269]