import requests
import ujson
import os

from time import sleep

from drive_manager import WebDriverManager
from utils import load_cfg, save_cfg

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cfg = load_cfg()


class VulcanAuth:
    global cfg

    def __init__(
        self: webdriver,
        username: str,
        password: str,
        cookies: dict,
        school_url,
        symbol: str,
        driver: WebDriverManager,
    ):
        self.username = username
        self.password = password
        self.cookies = cookies
        self.school_url = school_url
        self.symbol = symbol
        self.driver = driver

    # https://uonetplus-uczen.vulcan.net.pl/powiatchrzanowski/009583/LoginEndpoint.aspx
    def scrap_symbol_from_url(self, url: str) -> str:
        return url.split("/")[-2]

    def cookies_to_dict(self, cookies) -> dict:
        return {c["name"]: c["value"] for c in cookies}

    def get_saved_cookies(self) -> dict:
        if not os.path.exists("cookies.json"):
            return {}

        with open("cookies.json", "r") as f:
            cookies = ujson.load(f)
            f.close()

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

            try:
                d.find_element(By.CLASS_NAME, "loginButton ").click()
            except Exception as e:
                print(e)

            e = d.find_element(By.NAME, "LoginName")
            e.send_keys(self.username)

            e = d.find_element(By.NAME, "Password")
            e.send_keys(self.password)

            e.send_keys("\ue007")

            sleep(5)

            if self.symbol == "default":
                move_to_e_dziennik_button = d.find_element(
                    By.XPATH, "/html/body/div[1]/main/div[2]/div[3]/div[2]/a"
                )
                self.symbol = self.scrap_symbol_from_url(
                    move_to_e_dziennik_button.get_attribute("href")
                )

                cfg["vulcan"]["symbol"] = self.symbol
                save_cfg(cfg)

            WebDriverWait(d, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/main/div[2]/div[3]/div[2]/a/div/div/div[2]",
                    )
                )
            ).click()

            sleep(3)

            self.cookies = self.cookies_to_dict(d.get_cookies())

            kick_out += 1

        if kick_out < 3:
            self.save_cookies(self.cookies)

            return {"cookies": self.cookies, "symbol": self.symbol}

        return -1
