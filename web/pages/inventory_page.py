from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from web.pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_loaded(self):
        return self.is_visible(self.PAGE_TITLE) and self.text_of(self.PAGE_TITLE) == "Products"

    def item_names(self):
        return self.texts_of(self.ITEM_NAME)

    def item_prices(self):
        return [float(text.replace("$", "")) for text in self.texts_of(self.ITEM_PRICE)]

    def sort_by(self, option_value):
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option_value)
        return self

    def add_item_to_cart_by_name(self, item_name):
        slug = item_name.lower().replace(" ", "-")
        self.click_until((By.ID, "add-to-cart-" + slug), (By.ID, "remove-" + slug))
        return self

    def remove_item_from_cart_by_name(self, item_name):
        slug = item_name.lower().replace(" ", "-")
        self.click_until((By.ID, "remove-" + slug), (By.ID, "add-to-cart-" + slug))
        return self

    def cart_count(self):
        return int(self.text_of(self.CART_BADGE)) if self.is_visible(self.CART_BADGE) else 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
        return self

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return self
