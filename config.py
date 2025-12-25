from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
from typing import Iterable, List, Tuple

from dotenv import load_dotenv


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_MAINTENANCE_START_DATE = datetime(2024, 1, 1, 0, 0, 0)
DEFAULT_DEV_SECRET = "dev-change-me"


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _parse_csv(value: str | None) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_datetime(value: str | None, default: datetime) -> Tuple[datetime, List[str]]:
    if not value:
        return default, []
    try:
        return datetime.strptime(value, DATE_FORMAT), []
    except ValueError:
        return default, [
            f"Invalid MAINTENANCE_START_DATE '{value}'. Expected format {DATE_FORMAT}."
        ]


@dataclass(frozen=True)
class AppConfig:
    environment: str
    debug: bool
    testing: bool
    secret_key: str
    database_uri: str
    maintenance_start_date: datetime
    mail_server: str | None
    mail_port: int
    mail_use_tls: bool
    mail_username: str | None
    mail_password: str | None
    mail_default_sender: str | None
    admins: List[str]
    log_level: str
    rate_limit_storage_uri: str

    def to_flask_dict(self) -> dict:
        return {
            "ENV": self.environment,
            "DEBUG": self.debug,
            "TESTING": self.testing,
            "SECRET_KEY": self.secret_key,
            "DATABASE_URI": self.database_uri,
            "SQLALCHEMY_DATABASE_URI": self.database_uri,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "WTF_CSRF_ENABLED": not self.testing,
            "SESSION_COOKIE_HTTPONLY": True,
            "REMEMBER_COOKIE_HTTPONLY": True,
            "SESSION_COOKIE_SAMESITE": "Lax",
            "SESSION_COOKIE_SECURE": self.environment == "production",
            "REMEMBER_COOKIE_SECURE": self.environment == "production",
            "MAINTENANCE_START_DATE": self.maintenance_start_date,
            "MAIL_SERVER": self.mail_server,
            "MAIL_PORT": self.mail_port,
            "MAIL_USE_TLS": self.mail_use_tls,
            "MAIL_USERNAME": self.mail_username,
            "MAIL_PASSWORD": self.mail_password,
            "MAIL_DEFAULT_SENDER": self.mail_default_sender,
            "ADMINS": self.admins,
            "LOG_LEVEL": self.log_level,
            "RATELIMIT_STORAGE_URI": self.rate_limit_storage_uri,
        }


def load_config(
    environment: str | None = None,
    *,
    load_env: bool = True,
) -> Tuple[AppConfig, List[str]]:
    if load_env:
        load_dotenv()

    env = (environment or os.getenv("FLASK_ENV", "development")).lower()
    debug = _parse_bool(os.getenv("DEBUG"), default=env == "development")
    testing = env == "testing"

    secret_key = os.getenv("SECRET_KEY")
    warnings: List[str] = []
    if not secret_key:
        if env == "production":
            raise ValueError("SECRET_KEY must be set in production.")
        secret_key = DEFAULT_DEV_SECRET
        warnings.append("Using default SECRET_KEY. Set SECRET_KEY in your .env file.")

    database_uri = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URI") or "sqlite:///instance/app.db"
    maintenance_start_date, maintenance_warnings = _parse_datetime(
        os.getenv("MAINTENANCE_START_DATE"),
        DEFAULT_MAINTENANCE_START_DATE,
    )
    warnings.extend(maintenance_warnings)

    mail_server = os.getenv("MAIL_SERVER")
    mail_port = _parse_int(os.getenv("MAIL_PORT"), 587)
    mail_use_tls = _parse_bool(os.getenv("MAIL_USE_TLS"), True)
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_default_sender = os.getenv("MAIL_DEFAULT_SENDER")
    admins = _parse_csv(os.getenv("ADMINS") or os.getenv("ADMIN_EMAILS"))
    if not admins:
        admins = ["noreply@example.com"]
        warnings.append("ADMINS not set; defaulting to noreply@example.com.")

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    rate_limit_storage_uri = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

    config = AppConfig(
        environment=env,
        debug=debug,
        testing=testing,
        secret_key=secret_key,
        database_uri=database_uri,
        maintenance_start_date=maintenance_start_date,
        mail_server=mail_server,
        mail_port=mail_port,
        mail_use_tls=mail_use_tls,
        mail_username=mail_username,
        mail_password=mail_password,
        mail_default_sender=mail_default_sender,
        admins=admins,
        log_level=log_level,
        rate_limit_storage_uri=rate_limit_storage_uri,
    )

    return config, warnings
