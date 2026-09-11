from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first_name, last_name, zip_code):
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.ZIP_INPUT, zip_code)
        return self

    def continue_to_overview(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def error_text(self):
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE)


class CheckoutStepTwoPage(BasePage):
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    def subtotal(self):
        return float(self.text_of(self.ITEM_TOTAL).replace("Item total: $", ""))

    def tax(self):
        return float(self.text_of(self.TAX_LABEL).replace("Tax: $", ""))

    def total(self):
        return float(self.text_of(self.TOTAL_LABEL).replace("Total: $", ""))

    def finish(self):
        self.click(self.FINISH_BUTTON)
        return self


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def is_complete(self):
        return self.is_visible(self.COMPLETE_HEADER) and "Thank you" in self.text_of(self.COMPLETE_HEADER)
