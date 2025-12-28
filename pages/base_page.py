from typing import Literal, Optional
from playwright.sync_api import Page, Locator
from config.settings import DEFAULT_TIMEOUT, BASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = DEFAULT_TIMEOUT

    def navigate(self, path: str = "") -> None:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")

    def click(self, locator: Locator, timeout: Optional[int] = None) -> None:
        logger.info(f"Clicking element: {locator}")
        locator.click(timeout=timeout or self.timeout)

    def fill(self, locator: Locator, text: str, timeout: Optional[int] = None) -> None:
        logger.info(f"Filling element with text: {text}")
        locator.fill(text, timeout=timeout or self.timeout)

    def get_text(self, locator: Locator, timeout: Optional[int] = None) -> str:
        text = locator.text_content(timeout=timeout or self.timeout)
        logger.info(f"Got text: {text}")
        return text or ""

    def is_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        try:
            locator.wait_for(state="visible", timeout=timeout or self.timeout)
            return True
        except Exception:
            return False

    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        logger.info(f"Waiting for URL: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout or self.timeout)

    def wait_for_load_state(
        self, state: Literal["domcontentloaded", "load", "networkidle"] = "load"
    ) -> None:
        logger.info(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state)

    def take_screenshot(self, name: str, full_page: bool = True) -> bytes:
        logger.info(f"Taking screenshot: {name}")
        return self.page.screenshot(path=name, full_page=full_page)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def reload(self) -> None:
        logger.info("Reloading page")
        self.page.reload()

    def go_back(self) -> None:
        logger.info("Navigating back")
        self.page.go_back()

    def go_forward(self) -> None:
        logger.info("Navigating forward")
        self.page.go_forward()
