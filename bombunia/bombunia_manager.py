import requests
import ujson
import os
import datetime

from bs4 import BeautifulSoup




from auth import VulcanAuth
from drive_manager import WebDriverManager
from utils import load_cfg, get_header

import logging

__logger = logging.getLogger("Bombunia")
__logger.addHandler(logging.NullHandler())

cfg = load_cfg()

HEADERS = {
    "Host": "uonetplus-uczen.vulcan.net.pl",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "*/*",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "X-V-RequestVerificationToken": "0rcpQv4ZNqZi_MLZY-u0wVKTJuTseNSfXpx5s6SMDjcendZVfuhc7LcMN4e2ZMwDVUolfSWp7F-dZWeb2xHIr1KrsK6rbsvKwHWCwsVleOqYOi0D0",
    "X-V-AppGuid": "fc21b3089d2d9dc61c1cc83e6e382576",
    "X-V-AppVersion": "21.10.0010.47230",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "16",
    "Origin": "https://uonetplus-uczen.vulcan.net.pl",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://uonetplus-uczen.vulcan.net.pl",  # chyba nie istotne
    "Cookie": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
}


class Bombunia:
    def __init__(
        self,
        username: str = "",
        password: str = "",
        cookies: dict = {},
        school_url: str = "",
        school_alias: str = "",
        symbol: str = "default",
        **kwargs,
    ):
        self.driver = WebDriverManager().get_driver()

        self.username = username
        self.password = password
        self.cookies = cookies
        self.school_url = school_url
        self.school_alias = school_alias
        self.symbol = symbol
        self.school_pupil_url = kwargs.get("school_pupil_url", "")

        self.auth = VulcanAuth(
            username=self.username,
            password=self.password,
            cookies=self.cookies,
            school_url=self.school_url,
            symbol=cfg["vulcan"]["symbol"]
            if cfg["vulcan"]["symbol"] != "default"
            else "default",
            driver=self.driver,
        )

    def __dict__(self):
        return {
            "username": self.username,
            "cookies_length": len(self.cookies),
            "school_url": self.school_url,
            "symbol": self.symbol,
        }

    def init_session(self):
        """
        Creates a driver session and returns the cookies
        """

        x = self.auth.get_working_cookies()
        self.symbol = x["symbol"]

        return x

    def close_session(self):
        """
        Closes the driver session
        """

        self.driver.close()

    def _parse_cookies_for_header(self, cookies: dict) -> str:
        """
        Parses the cookies dict to a string
        """

        return "; ".join([f"{k}={v}" for k, v in cookies.items()])

    def _get_header(self, cookies: dict) -> dict:
        """
        Returns the header with the provided cookies
        """

        HEADERS["Cookie"] = self._parse_cookies_for_header(cookies)
        return HEADERS

    def grades_to_list(self, subject) -> list:
        """
        Parses grades from json to a list
        """

        _grades_to_list = []
        for i in range(0, 6):
            _grades_to_list.append(int(subject["ClassSeries"]["Items"][5 - i]["Value"]))

        return _grades_to_list

    def get_grades(self, **kwargs) -> list:
        """
        Gets the grades from the school_pupil_url
        """

        _grades_now = []
        payload = {
            "idOkres": 1048
            if kwargs.get("id_okres") == None
            else kwargs.get("id_okres")
        }

        try:
            r = requests.post(
                self.school_pupil_url,
                cookies=self.cookies,
                data=ujson.dumps(payload),
                headers=self._get_header(self.cookies),
            )
        except Exception as e:
            __logger.error(e)
            return -1

        r = r.json()

        sum_of_all_grades = 0
        count_of_all_grades = 0

        for subject in r["data"]:
            if subject["TableContent"] == None:
                _grades_now.append(
                    {"subject_name": subject["Subject"], "grades": [0, 0, 0, 0, 0, 0]}
                )
            else:
                _grades_now.append(
                    {
                        "subject_name": subject["Subject"],
                        "grades": self.grades_to_list(subject),
                    }
                )

                for idx, label in enumerate(subject["ClassSeries"]["Items"]):
                    sum_of_all_grades += int(label["Value"]) * (5 - idx)
                    count_of_all_grades += int(label["Value"])

        dt = datetime.datetime.now()

        _parsed_grades = []

        _parsed_grades.append(
            {
                "time": dt.timestamp(),
                "sum_of_all_grades": sum_of_all_grades,
                "count_of_all_grades": count_of_all_grades,
                "all_grades": _grades_now,
            }
        )

        return _parsed_grades

    def save_grades(self, grades: list, folder_path: str = "grades") -> None:
        """
        Saves the grades dict to a folder (with last grades file number + 1)
        """

        _number_of_files = len(os.listdir(folder_path))

        with open(f"{folder_path}/{_number_of_files + 1}.json", "w") as f:
            ujson.dump(grades, f)

    def get_last_grades(
        self, folder_path: str = "grades", file_offset: int = 0
    ) -> list:
        """
        Gets the last grades from the folder
        """

        _number_of_files = len(os.listdir(folder_path))

        if _number_of_files - file_offset > 0:
            with open(f"{folder_path}/{_number_of_files - file_offset}.json", "r") as f:
                return ujson.load(f)

        return -1

    def last_grades_list(
        self, folder_path: str = "grades", offset_from: int = 1, offset_to: int = 5
    ) -> list:
        """
        Gets the last five grades from the folder
        """

        _last_grades = []

        for i in range(offset_from, offset_to):
            _last_grades.append(self.get_last_grades(file_offset=i))

        return _last_grades

    def compare_grades(self, grades_a: list, grades_b: list) -> list:
        """
        Compares two grades lists, subtracts -> a - b
        """

        _differeces = []

        for idx, subject in enumerate(grades_a[0]["all_grades"]):
            if (
                subject["subject_name"]
                == grades_b[0]["all_grades"][idx]["subject_name"]
            ):
                _diff_grades = []

                for a, b in zip(
                    subject["grades"], grades_b[0]["all_grades"][idx]["grades"]
                ):
                    _diff_grades.append(a - b)

                _differeces.append(
                    {"subject_name": subject["subject_name"], "grades": _diff_grades}
                ) if sum(_diff_grades) != 0 else None

        return _differeces
