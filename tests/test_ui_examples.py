import pytest
import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.ui
class TestPlaywrightDemo:

    def test_has_title(self, page: Page):
        """Test that playwright.dev has the correct title."""
        logger.info("Starting test_has_title")
        base_page = BasePage(page)
        base_page.navigate("https://playwright.dev/")

        expect(page).to_have_title(re.compile("Playwright"))
        logger.info("Title assertion passed")

    def test_get_started_link(self, page: Page):
        """Test navigation to the installation page."""
        logger.info("Starting test_get_started_link")
        page.goto("https://playwright.dev/")

        page.get_by_role("link", name="Get started").click()
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()
        logger.info("Navigation and heading assertion passed")

    @pytest.mark.slow
    def test_search_functionality(self, page: Page):
        logger.info("Starting test_search_functionality")
        page.goto("https://playwright.dev/")

        search_button = page.get_by_role("button", name="Search")
        search_button.click()

        search_input = page.get_by_placeholder("Search docs")
        expect(search_input).to_be_visible()
        search_input.fill("test")

        page.wait_for_timeout(1000)
        logger.info("Search test completed")


@pytest.mark.regression
@pytest.mark.ui
class TestResponsiveDesign:
    @pytest.mark.parametrize(
        "viewport",
        [
            {"width": 375, "height": 667},
            {"width": 768, "height": 1024},
            {"width": 1920, "height": 1080},
        ],
    )
    def test_responsive_layout(self, page: Page, viewport):
        logger.info(f"Testing viewport: {viewport}")
        page.set_viewport_size(viewport)
        page.goto("https://playwright.dev/")

        expect(page).to_have_title(re.compile("Playwright"))
        logger.info(f"Responsive test passed for {viewport}")
