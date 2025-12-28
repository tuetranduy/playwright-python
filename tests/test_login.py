import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.helpers import read_json_file
from config.settings import TEST_DATA_DIR
from utils.logger import get_logger

logger = get_logger(__name__)

TEST_DATA = read_json_file(str(TEST_DATA_DIR / "users.json"))


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    """Login functionality tests."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup - navigate to login page."""
        # Update this URL to your actual login page
        self.login_page = LoginPage(page)
        # self.login_page.navigate("/login")

    @pytest.mark.skip(reason="Update with actual login page URL")
    def test_successful_login(self, page: Page):
        """Test successful login with valid credentials."""
        logger.info("Testing successful login")
        user = TEST_DATA["valid_user"]

        self.login_page.login(user["username"], user["password"])

        # Add assertions for successful login
        # e.g., check for dashboard URL, welcome message, etc.
        logger.info("Login test passed")

    @pytest.mark.skip(reason="Update with actual login page URL")
    def test_invalid_login(self, page: Page):
        """Test login with invalid credentials."""
        logger.info("Testing invalid login")
        user = TEST_DATA["invalid_user"]

        self.login_page.login(user["username"], user["password"])

        # Assert error message is displayed
        error_msg = self.login_page.get_error_message()
        assert len(error_msg) > 0
        logger.info(f"Error message displayed: {error_msg}")

    @pytest.mark.skip(reason="Update with actual login page URL")
    @pytest.mark.parametrize(
        "username,password,expected",
        [
            ("", "password", "username_required"),
            ("user@test.com", "", "password_required"),
            ("", "", "both_required"),
        ],
    )
    def test_login_validation(self, page: Page, username, password, expected):
        """Test login field validation."""
        logger.info(f"Testing validation: {expected}")

        self.login_page.login(username, password)

        # Add validation assertions based on expected behavior
        logger.info(f"Validation test passed: {expected}")
