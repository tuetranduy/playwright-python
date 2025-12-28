import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEST_DATA_DIR = DATA_DIR / "test_data"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

ENV = os.getenv("TEST_ENV", "qa")

BASE_URLS = {
    "dev": "https://dev.example.com",
    "qa": "https://qa.example.com",
    "staging": "https://staging.example.com",
    "prod": "https://example.com"
}

BASE_URL = os.getenv("BASE_URL", BASE_URLS.get(ENV, BASE_URLS["qa"]))

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
DEFAULT_NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
BROWSER = os.getenv("BROWSER", "chromium")

SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
SCREENSHOT_DIR = REPORTS_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_ON = os.getenv("VIDEO_ON", "false").lower() == "true"
VIDEO_DIR = REPORTS_DIR / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

TRACE_ON = os.getenv("TRACE_ON", "retain-on-failure")

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30000"))
API_BASE_URL = os.getenv("API_BASE_URL", f"{BASE_URL}/api")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "test_db")
DB_USER = os.getenv("DB_USER", "test_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "test_password")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / f"test_run_{ENV}.log"
