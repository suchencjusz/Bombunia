from loguru import logger

import time
import requests
import ujson
import base64
import hikari

from utils import load_cfg
from bombunia_manager import Bombunia
from analyzer import Analyzer

cfg = load_cfg()

if __name__ == "__main__":
    logger.add("logs/{time}.txt", rotation="1 day", retention="6 month", enqueue=True)
    logger.success(f"Bombunia started - version: {cfg['version']}")



    # b = Bombunia(
    #     username=cfg["vulcan"]["username"],
    #     password=cfg["vulcan"]["password"],
    #     cookies={},
    #     school_url=cfg["vulcan"]["school_url"],
    #     school_alias=cfg["vulcan"]["school_alias"],
    #     symbol=cfg["vulcan"]["symbol"],
    #     school_pupil_url=cfg["vulcan"]["school_pupil_url"],
    # )

    # x = b.init_session()
    # b.close_session()

    # b.symbol = x["symbol"]
    # b.cookies = x["cookies"]

    # b.school_pupil_url = f"{b.school_pupil_url}{b.school_alias}/{b.symbol}/Statystyki.mvc/GetOcenyCzastkowe"

    # _grades_now = b.get_grades(id_okres=1048)
    # _grades_before = b.get_last_grades()

    # _difference = b.compare_grades(_grades_now, _grades_before)

    # if len(_difference) != 0:
    #     b.save_grades(_grades_now)



    #     for d in _difference:
    #         print(d['subject_name'], d['grades'])

    # _last_grades_set = b.last_grades_list()

    # chart1 = Analyzer().graph_from_list(_last_grades_set)

    # # save base64 image to png file
    # with open("chart1.png", "wb") as fh:
    #     fh.write(base64.b64decode(chart1))

    # print(b.__dict__())
