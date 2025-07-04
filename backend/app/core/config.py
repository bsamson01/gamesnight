from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")
    
    # JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # PayPal
    PAYPAL_CLIENT_ID: str = Field(..., env="PAYPAL_CLIENT_ID")
    PAYPAL_CLIENT_SECRET: str = Field(..., env="PAYPAL_CLIENT_SECRET")
    PAYPAL_MODE: str = Field(default="sandbox", env="PAYPAL_MODE")
    
    # App
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:5173"], env="CORS_ORIGINS")
    SENTRY_DSN: str = Field(default="", env="SENTRY_DSN")
    
    # Admin
    ADMIN_EMAIL: str = Field(default="admin@gamesnight.com", env="ADMIN_EMAIL")
    ADMIN_PASSWORD: str = Field(default="changeme", env="ADMIN_PASSWORD")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "CORS_ORIGINS":
                return [origin.strip() for origin in raw_val.split(",")]
            return raw_val


settings = Settings()