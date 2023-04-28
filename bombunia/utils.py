import ujson
import random
import string
from base64 import b64encode

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


config = load_cfg()


def create_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


# def send():
#     headers = {"Authorization": f"Client-ID {config['imgur']['client_imgur']}"}

#     api_key = config['api_key_imgur']

#     url = "https://api.imgur.com/3/upload.json"

#     j1 = requests.post(
#         url,
#         headers = headers,
#         data = {
#             'key': api_key,
#             'image': b64encode(open('last_stats.png', 'rb').read()),
#             'type': 'base64',
#             'name': 'last_stats.jpg',
#             'title': f'{create_random_string(10)}'
#         }
#     )

#     return j1.text
