# settings.py
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()  # Load variables from a local .env if present

import os
from typing import Optional

def _bool(val: Optional[str], default: bool = False) -> bool:
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}

@dataclass(frozen=True)
class Settings:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "CHANGE_ME__GENERATE_A_RANDOM_32_CHAR_SECRET")
    BASE_URL: str = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

    FULL_NAME: str = os.environ.get("FULL_NAME", "Kevin León")
    TAGLINE: str = os.environ.get("TAGLINE", "IE Madrid • MSFT alum • Tech + Business")
    LINKEDIN_URL: str = os.environ.get("LINKEDIN_URL", "https://www.linkedin.com/in/your-handle")
    WHATSAPP_NUMBER: str = os.environ.get("WHATSAPP_NUMBER", "34600000000")
    EMAIL_ADDRESS: str = os.environ.get("EMAIL_ADDRESS", "you@example.com")
    INSTAGRAM_URL: str = os.environ.get("INSTAGRAM_URL", "https://www.instagram.com/your-handle")
    CV_URL: str = os.environ.get("CV_URL", "")

    ANALYTICS_DOMAIN: str = os.environ.get("ANALYTICS_DOMAIN", "")
    PRODUCTION: bool = _bool(os.environ.get("PRODUCTION"), default=False)

    # Default to friend view
    DEFAULT_AUDIENCE: str = os.environ.get("DEFAULT_AUDIENCE", "friend")  # "recruiter" | "friend"

SETTINGS = Settings()
