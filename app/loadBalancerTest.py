import requests
import os
from dotenv import load_dotenv

params = {
    "query": load_dotenv('query'),
    "limit": 100,
    "direction": "backward",
}

auth = (
    load_dotenv('GRAFANACLOUD_USERNAME'),
    load_dotenv('GRAFANACLOUD_PASS')
)

headers = {
    "Authorization": f"Bearer {bearer_token}"
}

response = requests.get(load_dotenv('loki_url'), params=params,auth=auth)

if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    print("Error:", response.status_code,", ", response.reason, ",", response._content)