import pytest

from config.settings import settings
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage


@pytest.mark.web
@pytest.mark.smoke
def test_valid_login_shows_products_page(driver):
    login_page = LoginPage(driver).load()
    login_page.login(settings.SAUCE_USERNAME, settings.SAUCE_PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()
    assert "/inventory.html" in driver.current_url


@pytest.mark.web
@pytest.mark.regression
def test_locked_out_user_sees_error(driver):
    login_page = LoginPage(driver).load()
    login_page.login("locked_out_user", settings.SAUCE_PASSWORD)

    assert login_page.has_error()
    assert "locked out" in login_page.error_text().lower()


@pytest.mark.web
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("invalid_user", "wrong_password", "do not match"),
    ],
)
def test_invalid_login_shows_expected_error(driver, username, password, expected_message):
    login_page = LoginPage(driver).load()
    login_page.login(username, password)

    assert login_page.has_error()
    assert expected_message.lower() in login_page.error_text().lower()


@pytest.mark.web
@pytest.mark.regression
def test_logout_returns_to_login_page(driver):
    login_page = LoginPage(driver).load()
    login_page.login(settings.SAUCE_USERNAME, settings.SAUCE_PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.logout()

    assert driver.current_url.rstrip("/") == settings.WEB_BASE_URL.rstrip("/")
