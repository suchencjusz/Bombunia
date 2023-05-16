import logging

__logger = logging.getLogger("Bombunia")
__logger.addHandler(logging.NullHandler())

from PIL import Image
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


    # _grades_now = b.get_last_grades(file_offset=1)
    # _grades_before = b.get_last_grades()

    # _difference = b.compare_grades(_grades_before, _grades_now, save_grades_a=False)

    # im = a.pie_differences_summary(_difference)
    # im.show()

    # for i in _difference:
    #     print(i["subject_name"], i["grades"])


    _x = b.get_all_grades()

    _x = a.graph_from_list(_x)

    _x.show()













    # if len(_difference) != 0:
    #     b.save_grades(_grades_now)


    # x = b.init_session()
    # b.close_session()

    

    # b.symbol = x["symbol"]
    # b.cookies = x["cookies"]

    # x = b.get_grades(id_okres=1048)

    # b.init_grades_folder(x)

    # for d in _difference:
    #     print(d['subject_name'], d['grades'])

   
    