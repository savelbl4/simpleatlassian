import browser_cookie3
import requests
from typing import Optional
from atlassian import Confluence, Jira

from ..config.config import config
from .exceptions import AuthenticationError
from .session import create_secure_session
from ..services.jira_service import JiraService
from ..services.confluence_service import ConfluenceService


class AtlassianAuth:
    """Authentication manager for Atlassian services."""

    def __init__(self):
        self._session: Optional[requests.Session] = None
        self._service = None

    def get_session(self) -> requests.Session:
        """Get authenticated session."""
        self._session = create_secure_session()

        if config.use_browser_cookies:
            self._authenticate_with_browser_cookies()
        else:
            self._authenticate_with_token()

        return self._session

    def _authenticate_with_token(self):
        """Authenticate using API token."""
        self._session.auth = (config.atlassian_username, config.atlassian_token)

    def _authenticate_with_browser_cookies(self):
        """Authenticate using browser cookies."""
        try:
            domain_name = self._service + config.atlassian_url.split('/')[-1]
            cj = browser_cookie3.chrome(domain_name=domain_name)
            self._session.cookies.update(cj)
        except Exception as e:
            raise AuthenticationError(f"Failed to get browser cookies: {e}")

    def create_confluence_client(self, **kwargs) -> Confluence:
        """Create Confluence client."""
        self._service = "confluence."
        session = self.get_session()

        client = Confluence(
            url=config.atlassian_url.replace('//', '//' + self._service),
            session=session,
            verify_ssl=config.verify_ssl,
            **kwargs
        )

        ConfluenceService(client).test_connection()
        return client

    def create_jira_client(self, **kwargs) -> Jira:
        """Create Jira client."""
        self._service = "jira."
        session = self.get_session()

        client = Jira(
            url=config.atlassian_url.replace('//', '//' + self._service),
            session=session,
            verify_ssl=config.verify_ssl,
            **kwargs
        )

        JiraService(client).test_connection()
        return client

# Global auth instance
auth = AtlassianAuth()
