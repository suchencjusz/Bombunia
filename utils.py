import ujson

import json
import requests
import random
import string
from base64 import b64encode

def load_cfg():
    with open("config.json", "r") as f:
        cfg = ujson.load(f)
        f.close()
    return cfg

config = load_cfg()

def create_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
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