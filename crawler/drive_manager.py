from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


class WebDriverManager:
    def __init__(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Firefox(
            options=options, service=FirefoxService(GeckoDriverManager().install())
        )

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.close()
