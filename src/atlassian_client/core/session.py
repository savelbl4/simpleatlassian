import requests
import urllib3
from requests import adapters
from ..config.config import config

# Отключаем SSL предупреждения если нужно
if not config.verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_secure_session() -> requests.Session:
    """Create configured requests session."""
    session = requests.Session()

    # Configuration
    session.verify = config.verify_ssl
    session.timeout = config.request_timeout

    # Headers
    session.headers.update({
        'User-Agent': 'Atlassian-Client/0.1.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    })

    # Retry strategy
    adapter = adapters.HTTPAdapter(max_retries=config.max_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session
