import logging
from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration class that loads environment variables
    for database, authentication, email, and logging settings.
    """

    # =============================
    # Application settings
    # =============================
    APP_NAME: str = "FastAPI Clean Architecture Template"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # =============================
    # Database settings
    # =============================
    DATABASE_URL: str = "sqlite:///./database.db"
    DB_ECHO: bool = False  # Enables SQLModel echo logs if True

    # =============================
    # Authentication / Security settings
    # =============================
    SECRET_KEY: str = "secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # =============================
    # Admin user settings
    # =============================
    ADMIN_USER: str = "admin"
    ADMIN_EMAIL: EmailStr = "admin@example.com"
    ADMIN_PASSWORD: str = "admin"
    ADMIN_FULL_NAME: str = "Admin"

    # =============================
    # Email settings
    # =============================
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[EmailStr] = None

    # =============================
    # Logging settings
    # =============================
    LOG_LEVEL: int = logging.INFO
    LOG_FILE: str = "logs/app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, env_file_encoding="utf-8"
    )


settings = Settings()
