"""
Enhanced configuration settings for FitCoach AI.

Provides comprehensive application configuration with validation
and environment-aware settings.
"""

import os
from typing import List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    All settings can be overridden via environment variables.
    """
    
    # Application Info
    PROJECT_NAME: str = "FitCoach AI"
    VERSION: str = "2.0.0"
    DESCRIPTION: str = "Professional fitness analytics and coaching platform"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database Configuration
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "fitcoach"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components."""
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    # JWT Authentication
    SECRET_KEY: str = "change-this-in-production-to-a-random-secret-key-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]
    ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_DEFAULT: str = "200/minute"
    RATE_LIMIT_AUTH: str = "5/minute"
    RATE_LIMIT_WRITE: str = "30/minute"
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DIR: str = "logs"
    
    # Pagination Defaults
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Fitness Calculation Constants
    FITNESS_WEEKLY_LOSS_RATE: float = 0.45  # kg per week for cuts
    FITNESS_WEEKLY_GAIN_RATE: float = 0.25  # kg per week for bulks
    FITNESS_CUT_DEFICIT: int = 500  # calorie deficit
    FITNESS_BULK_SURPLUS: int = 350  # calorie surplus
    
    # Feature Flags
    ENABLE_ANALYTICS: bool = True
    ENABLE_WORKOUT_GENERATOR: bool = True
    ENABLE_PROGRESS_INSIGHTS: bool = True
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Warn if using default secret key."""
        if "change-this" in v.lower() and os.getenv("SECRET_KEY") is None:
            import warnings
            warnings.warn(
                "Using default SECRET_KEY. Set a secure SECRET_KEY "
                "environment variable in production!",
                UserWarning
            )
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are only loaded once.
    
    Returns:
        Settings instance
    """
    return Settings()


# Export singleton instance for convenience
settings = get_settings()


# Environment helpers
def is_production() -> bool:
    """Check if running in production environment."""
    return not settings.DEBUG


def is_development() -> bool:
    """Check if running in development environment."""
    return settings.DEBUG
