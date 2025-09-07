from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App
    debug: bool = True
    host: str = "0.0.0.0"  # Bind to all interfaces
    port: int = 8000
    
    # Network Configuration
    allowed_hosts: list = ["*"]  # CORS allowed origins
    workers: int = 1  # Number of worker processes
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
