import requests
import os
from dotenv import load_dotenv

loki_url = "http://logs-prod-025.grafana.net/loki/api/v1/query_range"
query ='{application="workload"} |= `` | sort_desc'

params = {
    "query": query,
    "limit": 100,
    "direction": "backward",
}

auth = (
    load_dotenv('GRAFANACLOUD_USERNAME'),
    load_dotenv('GRAFANACLOUD_PASS')
)

response = requests.get(loki_url, params=params,auth=auth)

if response.status_code == 200:
    # Print the response content
    print(response.json())
else:
    print("Error:", response.status_code,", ", response.reason, ",", response._content)