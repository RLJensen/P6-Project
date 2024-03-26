import requests
import numpy as np

def evaluate_population(subpopulation, distances):
    total_distances = []
    for route in subpopulation:
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += distances[route[i]][route[i + 1]]
        total_distance += distances[route[-1]][route[0]]  # Return to starting city
        total_distances.append(total_distance)
    return total_distances

def send_results(results):
    url = "http://master-service:5000/collect-results"
    response = requests.post(url, json=results)
    return response.status_code

if __name__ == "__main__":
    # Get tasks from master
    url = "http://master-service:5000/distribute-tasks"
    response = requests.post(url, json={"population": ..., "num_workers": ...})
    tasks = response.json()

    # Evaluate tasks
    distances = ...  # Distance matrix
    evaluated_populations = []
    for task in tasks:
        evaluated_populations.append(evaluate_population(task, distances))

    # Send evaluated populations back to master
    send_results(evaluated_populations)
