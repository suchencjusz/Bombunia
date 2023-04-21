import base64
import json
import requests
import random
import string
from base64 import b64encode

with open('config.json') as f:
    config = json.load(f)
    f.close()

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def discord_send() -> requests.Response:
    headers = {"Authorization": f"Client-ID {config['imgur']['client_id']}"}

    api_key = config['imgur']['client_secret']

    url = "https://api.imgur.com/3/upload.json"

    r = requests.post(
        url, 
        headers = headers,
        data = {
            'key': api_key, 
            'image': b64encode(open('last_stats.png', 'rb').read()),
            'type': 'base64',
            'name': 'last_stats.jpg',
            'title': f'{get_random_string(10)}'
        }
    )

    return r