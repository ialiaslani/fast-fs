from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = True

    class Config:
        env_file = ".env"  # Optional, for local testing

settings = Settings()