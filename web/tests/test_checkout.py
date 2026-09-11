import pytest

from config.settings import settings
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


@pytest.fixture
def checkout_step_one(driver):
    login_page = LoginPage(driver).load()
    login_page.login(settings.SAUCE_USERNAME, settings.SAUCE_PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.go_to_cart()

    CartPage(driver).checkout()
    return CheckoutStepOnePage(driver)


@pytest.mark.web
@pytest.mark.smoke
def test_complete_checkout_flow_succeeds(checkout_step_one, driver):
    checkout_step_one.fill_info("Jane", "Doe", "12345")
    checkout_step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(driver)
    assert round(step_two.subtotal() + step_two.tax(), 2) == round(step_two.total(), 2)

    step_two.finish()

    assert CheckoutCompletePage(driver).is_complete()


@pytest.mark.web
@pytest.mark.regression
@pytest.mark.parametrize(
    "first_name, last_name, zip_code, expected_message",
    [
        ("", "Doe", "12345", "First Name is required"),
        ("Jane", "", "12345", "Last Name is required"),
        ("Jane", "Doe", "", "Postal Code is required"),
    ],
)
def test_checkout_requires_all_fields(checkout_step_one, first_name, last_name, zip_code, expected_message):
    checkout_step_one.fill_info(first_name, last_name, zip_code)
    checkout_step_one.continue_to_overview()

    assert checkout_step_one.has_error()
    assert expected_message.lower() in checkout_step_one.error_text().lower()
