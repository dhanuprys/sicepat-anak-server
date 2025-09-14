"""
Configuration settings for Stunting Checking App
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@db:3306/stunting_db")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Base URL settings
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    
    # Add production origins if in production
    if ENVIRONMENT == "production":
        CORS_ORIGINS.extend([
            "https://stunting-api.dedan.my.id",
            "https://your-frontend-domain.com"
        ])
    
    # Reports directory
    REPORTS_DIR: str = "reports"
    
    # ML Model settings
    MODEL_CACHE_DIR: str = "model_cache"
    MODEL_FILE: str = "stunting_predictor.pkl"

# Create global settings instance
settings = Settings()