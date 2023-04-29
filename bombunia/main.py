import logging

__logger = logging.getLogger("Bombunia")
__logger.addHandler(logging.NullHandler())

import time
import requests
import ujson
import base64
# import hikari

from utils import load_cfg
from bombunia_manager import Bombunia
from analyzer import Analyzer

cfg = load_cfg()

if __name__ == "__main__":
    __logger.info(f"Bombunia started - version: {cfg['version']}")



    b = Bombunia(
        username=cfg["vulcan"]["username"],
        password=cfg["vulcan"]["password"],
        cookies={},
        school_url=cfg["vulcan"]["school_url"],
        school_alias=cfg["vulcan"]["school_alias"],
        symbol=cfg["vulcan"]["symbol"],
    )

    a = Analyzer()

    x = b.init_session()
    b.close_session()

    

    b.symbol = x["symbol"]
    b.cookies = x["cookies"]

    x = b.get_grades(id_okres=1048)

    b.init_grades_folder(x)

    _grades_now = x
    _grades_before = b.get_last_grades()

    _difference = b.compare_grades(_grades_now, _grades_before)

    # if len(_difference) != 0:
    #     b.save_grades(_grades_now)



    for d in _difference:
        print(d['subject_name'], d['grades'])

    x = a.pie_differences_summary(_difference)

    with open("chart1.png", "wb") as fh:
        fh.write(base64.b64decode(x))
    
    # _last_grades_set = b.last_grades_list()

    # chart1 = Analyzer().graph_from_list(_last_grades_set)

    # # save base64 image to png file
    # with open("chart1.png", "wb") as fh:
    #     fh.write(base64.b64decode(chart1))

    # print(b.__dict__())
