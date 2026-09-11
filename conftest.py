import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.settings import settings

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")


@pytest.fixture
def driver():
    options = ChromeOptions()
    if settings.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    drv = webdriver.Chrome(options=options)
    drv.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"{item.name}-{timestamp}.png"
            path = os.path.join(SCREENSHOT_DIR, filename)
            try:
                driver_fixture.save_screenshot(path)
                report.sections.append(("Screenshot", path))
            except Exception:
                pass
