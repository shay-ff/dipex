import os
from os import environ
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    database_url: str = environ.get("DATABASE_URL")
    database_host: str = environ.get("DATABASE_HOST")
    database_port: int = environ.get("DATABASE_PORT")
    database_name: str = environ.get("DATABASE_DB")
    database_user: str = environ.get("DATABASE_USER")
    database_password: str = environ.get("DATABASE_PASSWORD")
    
    # JWT settings
    secret_key: str = environ.get("SECRET_KEY")
    algorithm: str = environ.get("ALGORITHM")
    access_token_expire_minutes: int = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # App settings
    app_name: str = environ.get("APP_NAME")
    debug: bool = environ.get("DEBUG")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
