import pytest

from config.settings import settings
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage


@pytest.fixture
def inventory_page(driver):
    login_page = LoginPage(driver).load()
    login_page.login(settings.SAUCE_USERNAME, settings.SAUCE_PASSWORD)
    return InventoryPage(driver)


@pytest.mark.web
@pytest.mark.smoke
def test_add_item_to_cart_updates_badge(inventory_page):
    assert inventory_page.cart_count() == 0

    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")

    assert inventory_page.cart_count() == 1


@pytest.mark.web
@pytest.mark.regression
def test_remove_item_from_cart_clears_badge(inventory_page):
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    assert inventory_page.cart_count() == 1

    inventory_page.remove_item_from_cart_by_name("Sauce Labs Backpack")

    assert inventory_page.cart_count() == 0


@pytest.mark.web
@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_option, key, reverse",
    [
        ("az", "name", False),
        ("za", "name", True),
        ("lohi", "price", False),
        ("hilo", "price", True),
    ],
)
def test_sorting_orders_products_correctly(inventory_page, sort_option, key, reverse):
    inventory_page.sort_by(sort_option)

    if key == "name":
        values = inventory_page.item_names()
    else:
        values = inventory_page.item_prices()

    assert values == sorted(values, reverse=reverse)


@pytest.mark.web
@pytest.mark.regression
def test_multiple_items_can_be_added_to_cart(inventory_page):
    items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    for item in items:
        inventory_page.add_item_to_cart_by_name(item)

    assert inventory_page.cart_count() == len(items)
