import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized, safe configuration management for the AI platform."""
    
    # ----------------------------------------------------
    # ENVIRONMENT SETTINGS
    # ----------------------------------------------------
    # Enables aggressive auto-healing (drop/recreate tables) if set to true.
    DEV_MODE = os.getenv("DEV_MODE", "false").strip().lower() == "true"
    
    # ----------------------------------------------------
    # AI PROVIDER CONFIGURATION
    # ----------------------------------------------------
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    
    # ----------------------------------------------------
    # DATABASE CONFIGURATION
    # ----------------------------------------------------
    _raw_db_url = os.getenv("DATABASE_URL", "").strip()
    
    # Safe Fallback Strategy
    if not _raw_db_url or "placeholder" in _raw_db_url.lower() or _raw_db_url == "postgresql://USER:PASSWORD@HOST:PORT/DB_NAME":
        DATABASE_URL = "sqlite:///./app.db"
    else:
        DATABASE_URL = _raw_db_url
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    @classmethod
    def get_status(cls):
        status = {
            "api_ready": bool(cls.GEMINI_API_KEY and "placeholder" not in cls.GEMINI_API_KEY.lower()),
            "db_mode": "SQLite (Local)" if "sqlite" in cls.DATABASE_URL else "PostgreSQL (Production)",
            "model": cls.GEMINI_MODEL,
            "dev_mode": cls.DEV_MODE
        }
        return status
