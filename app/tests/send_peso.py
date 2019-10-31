import requests

from core import config


data = {
    'reporter_id': 1,
    'kilos': 6,
    'gramos': 350
}

a = requests.post(f'http://{config.SERVER_NAME}{config.API_V1_STR}/peso/insert', json=data)
a.content
a.reason
dir(a)