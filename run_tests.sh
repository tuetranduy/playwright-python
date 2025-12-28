# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run UI tests only
pytest -m ui

# Run API tests only
pytest -m api

# Run in headed mode
pytest --headed

# Run with specific browser
pytest --browser firefox

# Run tests in parallel
pytest -n auto

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Run with Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Run specific test file
pytest tests/test_ui_examples.py

# Run specific test class
pytest tests/test_ui_examples.py::TestPlaywrightDemo

# Run specific test
pytest tests/test_ui_examples.py::TestPlaywrightDemo::test_has_title

# Debug mode (verbose with stdout)
pytest -v -s

# Run with custom environment
TEST_ENV=staging pytest

# Run with custom base URL
BASE_URL=https://example.com pytest
