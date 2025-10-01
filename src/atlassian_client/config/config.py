import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Загружаем .env файл
env_path = Path("~/.cfg/.env.atlassian").expanduser()
if env_path.exists():
    load_dotenv(env_path)
else:
    # Пробуем загрузить из текущей директории
    load_dotenv()


class AtlassianConfig(BaseModel):
    """Configuration for Atlassian services."""

    # Atlassian (делаем опциональными со значениями по умолчанию)
    atlassian_url: Optional[str] = Field(default=None, description="Atlassian instance URL")
    atlassian_username: Optional[str] = Field(default=None, description="Username or email")
    atlassian_token: Optional[str] = Field(default=None, description="API token or password")

    # Confluence
    confluence_space_key: Optional[str] = None

    # Jira
    jira_project_key: Optional[str] = None

    # App settings
    log_level: str = "INFO"
    request_timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = False
    use_browser_cookies: bool = False

    def is_configured(self) -> bool:
        """Check if minimal configuration is present."""
        return all([
            self.atlassian_url,
            self.atlassian_username,
            self.atlassian_token
        ])

    def validate_configuration(self) -> None:
        """Validate configuration and raise error if incomplete."""
        if not self.is_configured():
            missing = []
            if not self.atlassian_url:
                missing.append("ATLASSIAN_URL")
            if not self.atlassian_username:
                missing.append("ATLASSIAN_USERNAME")
            if not self.atlassian_token:
                missing.append("ATLASSIAN_TOKEN")

            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                f"Please set these environment variables or create a .env file"
            )


def load_config() -> AtlassianConfig:
    """Load configuration from environment variables."""
    pre_config = AtlassianConfig(
        atlassian_url=os.getenv('ATLASSIAN_URL'),
        atlassian_username=os.getenv('ATLASSIAN_USERNAME'),
        atlassian_token=os.getenv('ATLASSIAN_TOKEN'),
        confluence_space_key=os.getenv('CONFLUENCE_SPACE_KEY'),
        jira_project_key=os.getenv('JIRA_PROJECT_KEY'),
        log_level=os.getenv('LOG_LEVEL', 'INFO'),
        request_timeout=int(os.getenv('REQUEST_TIMEOUT', '30')),
        max_retries=int(os.getenv('MAX_RETRIES', '3')),
        verify_ssl=os.getenv('VERIFY_SSL', 'false').lower() == 'true',
        use_browser_cookies=os.getenv('USE_BROWSER_COOKIES', 'false').lower() == 'true'
    )
    pre_config.validate_configuration()
    return pre_config

# Global config instance
config = load_config()
