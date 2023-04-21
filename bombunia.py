from auth import VulcanAuth
from drive_manager import WebDriverManager

import requests
from bs4 import BeautifulSoup

class Bombunia:
    def __init__(self, username="", password="", cookies={}, school_url=""):
        self.driver = WebDriverManager().get_driver()

        self.username = username
        self.password = password
        self.cookies = cookies
        self.school_url = school_url

        self.auth = VulcanAuth(
            username=self.username,
            password=self.password,
            cookies=self.cookies,
            school_url=self.school_url,
            driver=self.driver,
        )

    def __dict__(self):
        return {
            "username": self.username,
            "cookies_length": len(self.cookies),
            "school_url": self.school_url,
        }

    def init_session(self):
        """
        Creates a driver session and returns the cookies
        """

        return self.auth.get_working_cookies()
    
    def close_session(self):
        """
        Closes the driver session
        """

        self.driver.close()

    def get_grades(self):
        