from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Library System"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://user:password@localhost/library_db"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
