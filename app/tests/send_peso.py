import requests

from core import config


data = {
    'kilos': 4,
    'gramos': 300
}

SERVER_NAME = config.SERVER_NAME
a = requests.post(f'http://{SERVER_NAME}/peso', data=data)
a.content
a.reason
dir(a)