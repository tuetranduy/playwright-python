import pytest
from pathlib import Path
from playwright.sync_api import Page, BrowserContext, Browser
from typing import Generator, Dict, Any
from config.settings import (
    SCREENSHOT_ON_FAILURE,
    SCREENSHOT_DIR,
    VIDEO_ON,
    VIDEO_DIR,
    TRACE_ON,
    HEADLESS,
    SLOW_MO
)
from utils.logger import get_logger
from utils.helpers import get_timestamp, sanitize_filename

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: Dict) -> Dict:
    """Configure browser launch arguments."""
    return {
        **browser_type_launch_args,
        "headless": HEADLESS,
        "slow_mo": SLOW_MO,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    """Configure browser context arguments."""
    context_args = {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }

    if VIDEO_ON:
        context_args["record_video_dir"] = str(VIDEO_DIR)
        context_args["record_video_size"] = {"width": 1920, "height": 1080}

    return context_args


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args: dict) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(**browser_context_args)

    if TRACE_ON != "off":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    if TRACE_ON == "on" or (TRACE_ON == "retain-on-failure" and hasattr(context, "_failed")):
        trace_name = f"trace_{get_timestamp()}.zip"
        trace_path = SCREENSHOT_DIR / trace_name
        context.tracing.stop(path=str(trace_path))
        logger.info(f"Trace saved: {trace_path}")
    elif TRACE_ON != "off":
        context.tracing.stop()

    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    page = context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed and SCREENSHOT_ON_FAILURE:
            page = None
            for fixture_name in item.fixturenames:
                if fixture_name == "page":
                    page = item.funcargs.get("page")
                    break

            if page:
                test_name = sanitize_filename(item.nodeid.replace("::", "_"))
                screenshot_name = f"{test_name}_{get_timestamp()}.png"
                screenshot_path = SCREENSHOT_DIR / screenshot_name

                try:
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info(f"Screenshot saved: {screenshot_path}")
                except Exception as e:
                    logger.error(f"Failed to take screenshot: {e}")

                if hasattr(page.context, "_failed"):
                    page.context._failed = True
                else:
                    setattr(page.context, "_failed", True)


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: Smoke test cases")
    config.addinivalue_line("markers", "regression: Regression test cases")
    config.addinivalue_line("markers", "ui: UI test cases")
    config.addinivalue_line("markers", "api: API test cases")
    config.addinivalue_line("markers", "integration: Integration test cases")
    config.addinivalue_line("markers", "slow: Slow running test cases")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    logger.info("=" * 80)
    logger.info("Test execution started")
    logger.info("=" * 80)
    yield
    logger.info("=" * 80)
    logger.info("Test execution completed")
    logger.info("=" * 80)
