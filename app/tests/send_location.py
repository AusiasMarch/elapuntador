import requests

url = 'https://elapuntador.ddns.net/api/v1/location/'
data = {
    'sujeto': 'Ausias',
    'location': 'Something'
}

a = requests.post(url, json=data)