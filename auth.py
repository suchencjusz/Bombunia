import requests
import ujson
import os

from time import sleep

from drive_manager import WebDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class VulcanAuth:
    def __init__(
        self,
        username: str,
        password: str,
        cookies: dict,
        school_url,
        driver: WebDriverManager,
    ):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.school_url = school_url
        self.driver = driver

    def cookies_to_dict(self, cookies) -> dict:
        return {c["name"]: c["value"] for c in cookies}

    def get_saved_cookies(self) -> dict:
        if not os.path.exists("cookies.json"):
            return {}

        with open("cookies.json", "r") as f:
            cookies = ujson.load(f)
            f.close()

        cookies = self.cookies_to_dict(cookies)

        return cookies

    def save_cookies(self, cookies) -> None:
        cookies = self.cookies if cookies is None else cookies

        with open("cookies.json", "w") as f:
            ujson.dump(self.cookies, f)
            f.close()

    def verify_cookies(self, cookies) -> bool:
        cookies = self.cookies if cookies is None else cookies

        r = requests.get(
            f"{self.school_url}Start.mvc/Index", cookies=cookies, allow_redirects=False
        )

        return r.status_code == 200

    def get_working_cookies(self) -> dict:
        kick_out = 0

        self.cookies = self.get_saved_cookies()

        while self.verify_cookies(self.cookies) is False and kick_out < 3:
            d = self.driver

            try:
                d.get(self.school_url)
            except TimeoutError as e:
                print(e)
                d.close()
                return None

            d.find_element_by_class_name("loginButton").click()

            e = d.find_element_by_name("LoginName")
            e.send_keys(self.username)

            e = d.find_element_by_name("Password")
            e.send_keys(self.password)

            e.send_keys("\ue007")

            sleep(5)

            WebDriverWait(d, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/main/div[2]/div[3]/div[2]/a/div/div/div[2]",
                    )
                )
            ).click()

            sleep(5)

            WebDriverWait(d, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ext-element-731"]'))
            ).click()

            self.cookies = self.cookies_to_dict(d.get_cookies())

            self.save_cookies(self.cookies)

            kick_out += 1

        if kick_out < 3:
            return self.cookies

        return -1
