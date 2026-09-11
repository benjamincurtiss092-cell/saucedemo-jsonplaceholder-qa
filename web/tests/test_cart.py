import pytest

from config.settings import settings
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage


@pytest.fixture
def cart_with_one_item(driver):
    login_page = LoginPage(driver).load()
    login_page.login(settings.SAUCE_USERNAME, settings.SAUCE_PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.go_to_cart()

    return CartPage(driver)


@pytest.mark.web
@pytest.mark.smoke
def test_cart_shows_added_item(cart_with_one_item):
    assert "Sauce Labs Backpack" in cart_with_one_item.item_names()


@pytest.mark.web
@pytest.mark.regression
def test_remove_item_from_cart_page(cart_with_one_item, driver):
    cart_with_one_item.remove_item_from_cart_by_name("Sauce Labs Backpack")

    assert cart_with_one_item.item_names() == []


@pytest.mark.web
@pytest.mark.regression
def test_continue_shopping_returns_to_inventory(cart_with_one_item, driver):
    cart_with_one_item.continue_shopping()

    assert "/inventory.html" in driver.current_url
