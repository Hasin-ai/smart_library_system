from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Service Information
    SERVICE_NAME: str = "Loan Service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8003
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5434/loan_db"
    
    # External Services
    USER_SERVICE_URL: str = "http://localhost:8001"
    BOOK_SERVICE_URL: str = "http://localhost:8002"
    SERVICE_TIMEOUT: int = 30
    
    # Business Rules
    DEFAULT_LOAN_DAYS: int = 14
    MAX_EXTENSIONS: int = 2
    EXTENSION_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
