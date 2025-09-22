import os
from os import environ
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    database_url: str
    database_host: str
    database_port: int = 5432
    database_name: str
    database_user: str
    database_password: str
    
    # JWT settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App settings
    app_name: str = "Dipex"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
