import requests
import ujson
import logging
import datetime

from pymongo import MongoClient

from .auth import VulcanAuth
from .drive_manager import WebDriverManager
from utils import load_cfg


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
        mongodb: MongoClient = None,
        **kwargs,
    ):
        self.driver = WebDriverManager().get_driver()

        self.username = username
        self.password = password
        self.cookies = cookies
        self.school_url = school_url
        self.school_alias = school_alias
        self.symbol = symbol
        self.mongodb = mongodb

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
        self.cookies = x["cookies"]

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
        Gets the grades from the school_url
        """

        _school_pupil_url = (
            f"{self.school_url}{self.symbol}/Statystyki.mvc/GetOcenyCzastkowe"
        )

        _grades_now = []
        payload = {
            "idOkres": 1048
            if kwargs.get("id_okres") == None
            else kwargs.get("id_okres")
        }

        try:
            r = requests.post(
                _school_pupil_url,
                cookies=self.cookies,
                data=ujson.dumps(payload),
                headers=self._get_header(self.cookies),
            )
        except Exception as e:
            print(e)
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
                    sum_of_all_grades += int(label["Value"]) * (6 - idx)
                    count_of_all_grades += int(label["Value"])

        dt = datetime.datetime.now()

        _parsed_grades = {
            "time": dt,
            "sum_of_all_grades": sum_of_all_grades,
            "count_of_all_grades": count_of_all_grades,
            "all_grades": _grades_now,
        }

        return _parsed_grades

    def save_grades(self, grades: list) -> None:
        self.mongodb.insert_one(grades)

    @staticmethod
    def get_last_grades_from_db(_db: MongoClient) -> list:
        """
        Gets the last grades from the database
        """

        _r = _db.find_one(sort=[("time", -1)])

        return _r

    @staticmethod
    def get_all_grades_from_db(_db: MongoClient) -> list:
        """
        Gets every grade record from the database
        """
        _r = _db.find_many().sort("time", 1)

        return _r

    @staticmethod
    def get_difference_from_today(_db: MongoClient) -> list:
        newest_grades = Bombunia.get_last_grades_from_db(_db)
        newest_grades_day = newest_grades["time"].replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        yesterday_grades = _db.find_one(
            {"time": {"$lt": newest_grades_day}}, sort=[("time", -1)]
        )

        if yesterday_grades == None or newest_grades == None:
            return None

        difference = Bombunia.compare_grades(newest_grades, yesterday_grades)

        # difference['checked_time_a'] = yesterday_grades['time']
        # difference['checked_time_b'] = newest_grades['time']

        # difference.append(
        #     {
        #         "checked_time_a": yesterday_grades["time"],
        #         "checked_time_b": newest_grades["time"],
        #     }
        # )

        return difference

    @staticmethod
    def get_difference_from_date(_db: MongoClient, date: datetime) -> list:
        yesterday_grades = _db.find_one({"time": {"$lt": date}}, sort=[("time", -1)])

        date = date + datetime.timedelta(days=1)

        newest_grades = _db.find_one({"time": {"$lt": date}}, sort=[("time", -1)])

        if yesterday_grades == None or newest_grades == None:
            return None

        difference = Bombunia.compare_grades(newest_grades, yesterday_grades)

        if difference == [] or difference == None:
            return None

        # difference.append(
        #     {
        #         "checked_time_a": yesterday_grades["time"],
        #         "checked_time_b": newest_grades["time"],
        #     }
        # )

        return difference

    # @staticmethod
    # def get_difference_from_month_aggregation(
    #     _db: MongoClient, data_a: datetime, data_b: datetime
    # ) -> list:
    #     all_a = []
    #     all_b = []

    #     dt = _db.aggregate(
    #         [
    #             {"$match": {"time": {"$gte": data_a, "$lt": data_b}}},
    #             {
    #                 "$group": {
    #                     "_id": {
    #                         "year": {"$year": "$time"},
    #                         "month": {"$month": "$time"},
    #                         "day": {"$dayOfMonth": "$time"},
    #                     },
    #                     "oldestValue": {"$min": "$value"},
    #                     "all_grades": {"$push": "$all_grades"},
    #                 }
    #             },
    #             {
    #                 "$project": {
    #                     "date": {
    #                         "$dateFromParts": {
    #                             "year": "$_id.year",
    #                             "month": "$_id.month",
    #                             "day": "$_id.day",
    #                         }
    #                     },
    #                     "oldestValue": 1,
    #                     "all_grades": 1,
    #                     "_id": 0,
    #                 }
    #             },
    #         ]
    #     )

    #     for i in dt:
    #         x = len(i["all_grades"]) - 1

    #         d = i
    #         d["all_grades"][0] = i["all_grades"][x]

    #         all_a.append(d)

    #     print(all_a)

    #     all_b[0] = all_a[0]
    #     all_b = all_b + all_a[1:]

    #     diff = []

    #     for i in zip(all_a, all_b):
    #         x = Bombunia.compare_grades(i[0], i[1])

    #         print(len(i[0]), len(i[1]))

    #         print(x)

    #         if x != None:
    #             diff.append(x)

    #     print(diff)

    #     return diff
    @staticmethod
    def get_difference_in_days(date: datetime,d: int, _db: MongoClient):
        date = date - datetime.timedelta(days=d)

        r = []

        for i in range(7):
            date = date + datetime.timedelta(days=1)

            x = Bombunia.get_difference_from_date(_db, date)

            if x != None:
                r.append({"date": date.strftime("%Y-%m-%d"), "nd": i, "grades": x})
            else:
                continue

        return r

    @staticmethod

    # def generate_heatmap(compared_grades, subject=None):
    #     x = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    #     y = []

    #     # Find the range of dates in compared_grades
    #     min_date = None
    #     max_date = None
    #     for grade in compared_grades:
    #         date = datetime.datetime.strptime(grade["date"], "%Y-%m-%d")
    #         if min_date is None or date < min_date:
    #             min_date = date
    #         if max_date is None or date > max_date:
    #             max_date = date

    #     # Calculate the number of days between min_date and max_date
    #     num_days = (max_date - min_date).days + 1

    #     # Return blank array if no days provided
    #     if num_days == 0:
    #         return []

    #     # Initialize the heatmap with zeros
    #     heatmap = [[0] * num_days for _ in range(7)]

    #     for grade in compared_grades:
    #         date = datetime.datetime.strptime(grade["date"], "%Y-%m-%d")
    #         day = (date - min_date).days

    #         for g in grade["grades"]:
    #             if g["subject_name"] == subject or subject is None:
    #                 for idx, grd in enumerate(g["grades"]):
    #                     heatmap[day][idx] += grd

    #         y.append(date.strftime("%Y-%m-%d"))

    #     print(y)
    #     print(x)
    #     print()

    #     for i in range(len(x)):
    #         print(x[i], heatmap[i])

    #     return heatmap

    @staticmethod
    def compare_grades(grades_a: list, grades_b: list) -> list:
        """
        Compares two grades lists, subtracts -> a - b
        """

        try:
            x = grades_a["all_grades"]
            x = grades_b["all_grades"]
        except TypeError:
            return

        if grades_a["count_of_all_grades"] <= grades_b["count_of_all_grades"]:
            return

        _differences = []

        for idx, subject in enumerate(grades_a["all_grades"]):
            if subject["subject_name"] == grades_b["all_grades"][idx]["subject_name"]:
                _diff_grades = [
                    a - b
                    for a, b in zip(
                        subject["grades"], grades_b["all_grades"][idx]["grades"]
                    )
                ]

                if sum(_diff_grades) != 0:
                    _differences.append(
                        {
                            "subject_name": subject["subject_name"],
                            "grades": _diff_grades,
                        }
                    )

        return _differences

    @staticmethod
    def get_average_all(_db: MongoClient) -> list:
        """
        Gets the average of all grades
        """

        filter = {}
        project = {"time": 1, "sum_of_all_grades": 1, "count_of_all_grades": 1}
        sort = list({"time": 1}.items())

        _r = _db.find(filter=filter, projection=project, sort=sort)

        average = []

        for item in _r:
            average.append(
                {
                    item["time"]: item["sum_of_all_grades"]
                    / item["count_of_all_grades"],
                    "c": item["count_of_all_grades"],
                }
            )

        # for item in _r:
        #     average.extend({item["time"]: item["sum_of_all_grades"] / item["count_of_all_grades"]})

        return average
