"""
Configuration management for the Price Comparison Agent.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
    SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///price_history.db")
    
    # Scraping Configuration
    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "2"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))
    
    # Gemini Configuration
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
    GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    
    # Price Analysis
    PRICE_HISTORY_DAYS = int(os.getenv("PRICE_HISTORY_DAYS", "30"))
    MIN_PRICE_DROP_PERCENT = float(os.getenv("MIN_PRICE_DROP_PERCENT", "5"))
    
    # Platforms
    PLATFORMS = ["amazon", "flipkart", "meesho"]
    
    # Sale Events (Indian market)
    SALE_EVENTS = {
        "Republic Day Sale": {"month": 1, "days": [26]},
        "Valentine's Day Sale": {"month": 2, "days": [14]},
        "Holi Sale": {"month": 3, "days": list(range(15, 25))},
        "Summer Sale": {"month": 5, "days": list(range(1, 31))},
        "Independence Day Sale": {"month": 8, "days": [15]},
        "Ganesh Chaturthi Sale": {"month": 9, "days": list(range(1, 15))},
        "Diwali Sale": {"month": 10, "days": list(range(15, 31)) + list(range(1, 15))},
        "Black Friday": {"month": 11, "days": list(range(20, 30))},
        "Christmas Sale": {"month": 12, "days": list(range(20, 31))},
        "New Year Sale": {"month": 1, "days": list(range(1, 7))},
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required. Please set it in your .env file or environment variables."
            )
        return True
    
    @classmethod
    def get_headers(cls):
        """Get HTTP headers for requests"""
        return {
            "User-Agent": cls.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"⚠️  Configuration Warning: {e}")
