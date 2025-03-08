import requests

from flask import session

def get_data():
    response = requests.get('http://127.0.0.1:5000/')
    if response.status_code == 200:
        print('response.text')
        print(response.headers)

get_data()