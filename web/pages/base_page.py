from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import settings


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.DEFAULT_TIMEOUT)

    def open(self, path=""):
        self.driver.get(f"{settings.WEB_BASE_URL}{path}")
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        # zero matches is a valid result (e.g. an empty cart), not a timeout
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def click_until(self, click_locator, confirm_locator, attempts=3, confirm_gone=False):
        # native click() occasionally doesn't register in headless chrome; retry with
        # a JS-dispatched click if the expected state change hasn't happened yet
        condition = (
            EC.invisibility_of_element_located(confirm_locator)
            if confirm_gone
            else EC.presence_of_element_located(confirm_locator)
        )
        last_error = None
        for attempt in range(attempts):
            try:
                if attempt == 0:
                    self.click(click_locator)
                else:
                    self.driver.execute_script("arguments[0].click();", self.find(click_locator))
                self.wait.until(condition)
                return
            except (TimeoutException, StaleElementReferenceException) as exc:
                last_error = exc
        raise last_error

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def texts_of(self, locator, attempts=3):
        # elements can go stale between locating the list and reading .text off it
        for attempt in range(attempts):
            try:
                return [el.text for el in self.find_all(locator)]
            except StaleElementReferenceException:
                if attempt == attempts - 1:
                    raise

    def is_visible(self, locator):
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    @property
    def current_url(self):
        return self.driver.current_url
