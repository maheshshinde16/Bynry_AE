"""Environment configuration loaded from the shell or CI secret store."""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    web_base_url: str = os.getenv("WEB_BASE_URL", "https://app.qa.workflowpro.example")
    api_base_url: str = os.getenv("API_BASE_URL", "https://api.qa.workflowpro.example")
    ui_timeout_ms: int = int(os.getenv("UI_TIMEOUT_MS", "20000"))


settings = Settings()
