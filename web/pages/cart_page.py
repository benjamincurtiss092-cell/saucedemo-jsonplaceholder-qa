from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def item_names(self):
        return self.texts_of(self.CART_ITEM_NAME)

    def remove_item_from_cart_by_name(self, item_name):
        button_id = "remove-" + item_name.lower().replace(" ", "-")
        self.click_until((By.ID, button_id), (By.ID, button_id), confirm_gone=True)
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self
