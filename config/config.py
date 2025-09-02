import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") or ""

    # Retries
    MAX_SEARCH_RETRIES = 2      
    MAX_LLM_RETRIES = 5        

    # For Log
    LOG_FILE = os.path.join("logs", "log_2025-09-01.log")
