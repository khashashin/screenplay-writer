import secrets
from pathlib import Path
from typing import List, Union, Optional, Dict, Any

from pydantic import BaseSettings, AnyHttpUrl, PostgresDsn, validator, EmailStr


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)

    PROJECT_NAME: str = "Screenplay Writer API"
    PROJECT_DESCRIPTION: str = "Screenplay Writer API"
    PROJECT_VERSION: str = "0.0.1"

    PROJECT_DOMAIN: str = "localhost"
    COOKIE_DOMAIN: str = PROJECT_DOMAIN

    PROJECT_ADMIN_EMAIL: str
    PROJECT_ADMIN_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool = True

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASSWORD: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: Any = BASE_DIR / "/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    # 60 minutes * 24 hours * 8 days = 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    JWT_ACCESS_TOKEN_SECRET: str = SECRET_KEY + "access-token"
    JWT_REFRESH_TOKEN_SECRET: str = SECRET_KEY + "refresh-token"

    API_V1: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    LOG_LEVEL: str = "INFO"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        db_connection = PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            path=f"/{values.get('DB_NAME') or ''}",
        )
        return db_connection

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
