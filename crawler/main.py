from bombunia_manager import Bombunia
from auth import VulcanAuth
from utils import load_cfg

cfg = load_cfg()

from pymongo import MongoClient
from datetime import datetime, timedelta


class Crawler:
    def __init__(self):
        self.bombunia = Bombunia(
            username=cfg["vulcan"]["username"],
            password=cfg["vulcan"]["password"],
            cookies={},
            school_url=cfg["vulcan"]["school_url"],
            school_alias=cfg["vulcan"]["school_alias"],
            symbol=cfg["vulcan"]["symbol"],
        )

    def crawl_grades(self):
        self.bombunia.init_session()

        new_grades = self.bombunia.get_grades(id_okres=cfg["vulcan"]["id_okres"])

        self.bombunia.close_session()

        client = MongoClient(cfg["mongodb"]["url"])
        db = client[cfg["mongodb"]["db_name"]]
        db = db[cfg["mongodb"]["collection_name"]]

        self.bombunia.mongodb = db

        last_grades = self.bombunia.get_last_grades_from_db()

        _diff = self.bombunia.compare_grades(new_grades, last_grades)

        print()
        print("DIFF")
        print(_diff)

        if _diff != None and _diff != -1:
            self.bombunia.save_grades(new_grades)
            print("saved!")


if __name__ == "__main__":
    crw = Crawler()

    crw.crawl_grades()
