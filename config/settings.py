import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    WEB_BASE_URL = os.getenv("WEB_BASE_URL", "https://www.saucedemo.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    SAUCE_USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
    SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))


settings = Settings()
