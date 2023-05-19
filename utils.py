import ujson
import datetime

HEADERS = {
    "Host": "uonetplus-uczen.vulcan.net.pl",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "*/*",
    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "16",
    "Origin": "https://uonetplus-uczen.vulcan.net.pl",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://uonetplus-uczen.vulcan.net.pl",  # z tym tezz ale mniejszy
    "Cookie": "",
}


def get_header(cookies):
    HEADERS["Cookie"] = cookies
    return HEADERS


def load_cfg():
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
        f.close()
    return cfg


def save_cfg(cfg=load_cfg()):
    with open("config.json", "w") as f:
        ujson.dump(cfg, f)
        f.close()


def datetime_input_checker_n_parser(date: str) -> dict:
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except:
        return {"failed": True, "status": "invalid date format"}

    if date.date() > datetime.datetime.today().date():
        return {"failed": True, "status": "do not check the future >:c !!!"}

    return {"failed": False, "status": date}
