# from selenium import webdriver

# # from selenium.webdriver.chrome.service import Service as ChromeService
# # from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager


# class WebDriverManager:
#     def __init__(self):

#         options = webdriver.FirefoxOptions()
#         options.add_argument("--headless")


#         self.driver = webdriver.Firefox(
#             options=options,
#             service=FirefoxService(GeckoDriverManager().install())
#         )

#         # options = webdriver.ChromeOptions()
#         # options.add_argument("--headless")
#         # options.add_argument("--disable-gpu")
#         # options.add_argument("--no-sandbox")

#         # self.driver = webdriver.Chrome(
#         #     options=options, service=ChromeService(ChromeDriverManager().install())
#         # )

#     def get_driver(self):
#         return self.driver

#     def close_driver(self):
#         self.driver.close()


from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


class WebDriverManager:
    def __init__(self):
        options = Options()
        options.headless = True

        # self.driver = webdriver.Firefox(
        #     options=options, service=FirefoxService(GeckoDriverManager().install())
        # )

        self.driver = webdriver.Firefox(options=options)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.close()
