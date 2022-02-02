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

def send():
    headers = {"Authorization": f"Client-ID {config['client_imgur']}"}

    api_key = config['api_key_imgur']

    url = "https://api.imgur.com/3/upload.json"

    j1 = requests.post(
        url, 
        headers = headers,
        data = {
            'key': api_key, 
            'image': b64encode(open('zul.png', 'rb').read()),
            'type': 'base64',
            'name': 'zul.jpg',
            'title': f'{get_random_string(10)}'
        }
    )

    return j1.text