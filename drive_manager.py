from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


class WebDriverManager:
    def __init__(self):
        self.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.close()
