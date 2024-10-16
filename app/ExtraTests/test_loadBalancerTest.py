import requests
import os
from dotenv import load_dotenv
import pytest
import json

def test_load_balancing():
    days = "3d"
    get_logs(days)
    try:
        with open('test.json', 'r') as file:
            json_data = json.load(file)

        stream_objects = [stream['stream'] for stream in json_data['data']['result']]
        load_balancing_count = sum(1 for stream_obj in stream_objects if stream_obj['host'] != stream_obj['affinity'])

        print(f"Load balancing occurred {load_balancing_count} times out of {len(stream_objects)} instances. Over the past {days}.")
        # Perform assertions
        assert load_balancing_count > 0, "No load balancing occurrences detected!"
    except:
        print("Error loading test")
        assert False
    


def get_logs(days):
    loki_url = "http://logs-prod-025.grafana.net/loki/api/v1/query_range"
    query = '{application="Workload"} |= ``'
    load_dotenv()
    params = {
        "query": query,
        "limit": 1000,
        "direction": "backward",
        "since": days
    }

    auth = (
        os.environ['GRAFANACLOUD_USERNAME'],
        os.environ['GRAFANACLOUD_PASSWORD']
    )
    response = requests.get(loki_url, params=params,auth=auth)

    if response.status_code == 200:
        try:
            data = response.json()
            with open('test.json', 'w') as f:
                f.flush()  # Ensure all data is written to the file
                json.dump(data,f,indent=4)
            print("Data successfully written to test.json")
        except ValueError:
            print("Error: Response is not in JSON format")
        except IOError as e:
            print(f"IOError: {e}")
        
        print("data has been written successfully!")
    else:
        print("Error:", response.status_code,";", response.content,";", response.reason)
    
if __name__ == '__main__':
    test_load_balancing()