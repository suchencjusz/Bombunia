from pymongo import MongoClient

from utils import load_cfg
from bombunia.bombunia_manager import Bombunia

cfg = load_cfg()


class DBClient:
    def __init__(self) -> None:
        print("Initializing DBClient")

        DB_URI = cfg["mongodb"]["url"]
        if DB_URI is None:
            raise Exception("DB_URI is not defined")

        self.client = MongoClient(DB_URI)
        self.db = self.client.bombunia_dev.oceny

    def get_last_grades_from_db(self) -> list:
        return Bombunia.get_last_grades_from_db(self.db)

    def get_all_grades_from_db(self) -> list:
        return Bombunia.get_all_grades_from_db(self.db)

    def get_difference_from_today(self) -> list:
        return Bombunia.get_difference_from_today(self.db)

    def get_difference_from_date(self, date: str) -> list:
        return Bombunia.get_difference_from_date(self.db, date)
