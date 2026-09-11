from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CLASS_NAME, "error-button")

    def load(self):
        self.open("/")
        return self

    def login(self, username, password):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def error_text(self):
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self):
        return self.is_visible(self.ERROR_MESSAGE)
