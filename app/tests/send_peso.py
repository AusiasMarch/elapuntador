import requests

from core import config


data = {
    'reporter_id': 1,
    'kilos': 6,
    'gramos': 350
}

SERVER_NAME = config.SERVER_NAME
a = requests.post(f'http://{SERVER_NAME}/peso/insert', json=data)
a.content
a.reason
dir(a)