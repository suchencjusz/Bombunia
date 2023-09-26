import os

from selenium import webdriver

DOCKER_CONTAINER = os.environ.get("DOCKER_CONTAINER", False)


class WebDriverManager:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")

        print("DOCKER_CONTAINER", DOCKER_CONTAINER)

        if DOCKER_CONTAINER:
            self.driver = webdriver.Remote(
                command_executor="http://chrome:4444",
                options=chrome_options,
            )
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.implicitly_wait(30)

        self.driver = webdriver.Chrome(options=chrome_options)

        # options = Options()
        # options.headless = True

        # # self.driver = webdriver.Firefox(
        # #     options=options, service=FirefoxService(GeckoDriverManager().install())
        # # )

        # self.driver = webdriver.Firefox(options=options)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.close()
