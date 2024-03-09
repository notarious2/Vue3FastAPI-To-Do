import os
from pydantic_settings import BaseSettings



import os
from random import randint

from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    ENVIRONMENT: str = "development"
    # app settings
    ALLOWED_ORIGINS: str = "http://127.0.0.1:3000,http://localhost:3000"

    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "chat-postgres"
    DB_PORT: str = "5432"
    DB_NAME: str = "postgres"
    DB_SCHEMA: str = "chat"
    # specify single database url
    DATABASE_URL: str | None = None

    # authentication related
    JWT_ACCESS_SECRET_KEY: str = "9d9bc4d77ac3a6fce1869ec8222729d2"
    JWT_REFRESH_SECRET_KEY: str = "fdc5635260b464a0b8e12835800c9016"
    ENCRYPTION_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180
    NEW_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24



class TestSettings(GlobalSettings):
    DB_SCHEMA: str = f"test_{randint(1, 100)}"


class DevelopmentSettings(GlobalSettings):
    pass

class ProductionSettings(GlobalSettings):
    pass



def get_settings():
    env = os.environ.get("ENVIRONMENT", "development")
    if env == "test":
        return TestSettings()
    elif env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()

    return GlobalSettings()


settings = get_settings()
