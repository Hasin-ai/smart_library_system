from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Service Information
    SERVICE_NAME: str = "User Service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8001
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/user_db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
