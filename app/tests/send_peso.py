import requests

from core import config


data = {
    'reporter_id': 1,
    'kilos': 4,
    'gramos': 300
}

SERVER_NAME = config.SERVER_NAME
SERVER_NAME = 'elanotador.ddns.net'
a = requests.post(f'http://{SERVER_NAME}/peso', data=data)
a.content
a.reason
dir(a)