import requests
import json

def request(url, method, data=None, token=None):
    if data:
        payload = json.dumps(data)
    else:
        payload = {}
    if token:
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
    else:
        headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request(method, url, headers=headers, data=payload)
    return response
