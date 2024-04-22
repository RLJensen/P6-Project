from math import atan2, cos, radians, sin, sqrt
import numpy as np
import random
import itertools
import time
import logging
import logger
import uuid
import socket
import logging_loki
import os
from multiprocessing import Queue
from dotenv import load_dotenv

workload_type = "TSP"
uuid = str(uuid.uuid4())
hostname = socket.gethostname()

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.hostname = hostname
        record.workload_type = workload_type
        record.uuid = uuid
        return super().format(record)

def setup_logger():
    custom_logger = logging.getLogger()
    custom_logger.setLevel(logging.INFO)

    load_dotenv()

    if custom_logger.hasHandlers():
        custom_logger.handlers.clear()

    try:
        handler = logging_loki.LokiQueueHandler(
            Queue(), #halp får error Exception in thread Thread-1 (_monitor): Traceback (most recent call last):
            url=os.environ['GRAFANACLOUD_URL'],  # Directly accessing for immediate error on misconfig
            tags={"application": "Workload",
                  "host": hostname,
                  "workload": workload_type,
                  "uuid": uuid},
            auth=(os.environ['GRAFANACLOUD_USERNAME'], os.environ['GRAFANACLOUD_PASSWORD']),
            version="1",
        )
    except Exception as e:
        print(f"Failed to setup Loki handler: {str(e)}")  # Immediate feedback on failure
        raise
    
    formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(hostname)s - %(workload_type)s - %(uuid)s - %(message)s')
    handler.setFormatter(formatter)

    custom_logger.addHandler(handler)

# Read city coordinates from file
def read_city_coordinates(filename, num_cities):
    city_coordinates = {}
    with open(filename, 'r') as file:
        for line in file.readlines()[:num_cities]:
            parts = line.strip().split(',')
            city = parts[0]
            latitude = float(parts[1])
            longitude = float(parts[2])
            city_coordinates[city] = (latitude, longitude)
    return city_coordinates

# Define parameters for the algorithm
filename = 'cities.txt'
num_cities = random.randint(10, 100) # Specify the number of cities you want to select
logging.info(f"Number of cities: {num_cities}")
cities = read_city_coordinates(filename, num_cities)
population_size = random.randint(15, 20) # Number of routes in each generation
logging.info(f"Population size: {population_size}")
num_generations = 3 # Number of generations
logging.info(f"Number of generations: {num_generations}")

# Calculate distance between two cities
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Calculate Haversine distance between two cities
# This calculates the distance between two points on the surface of a sphere
def haversine_distance(city1, city2):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = radians(city1[0]), radians(city1[1])
    lat2, lon2 = radians(city2[0]), radians(city2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Calculate total distance of a route
def total_distance(route):
    total = 0
    for i in range(len(route) - 1):
        total += haversine_distance(cities[route[i]], cities[route[i+1]])
    total += haversine_distance(cities[route[-1]], cities[route[0]])
    return total

# Generate initial population
def generate_initial_population(population_size):
    cities_list = list(cities.keys())
    population = []
    for _ in range(population_size):
        route = random.sample(cities_list, len(cities_list))
        population.append(route)
    return population

# Evolve the population 
def evolve_population(subpopulation):
    offspring = []
    # Select routes for crossover
    selected_routes = random.sample(subpopulation, len(subpopulation) // 2)

    # Perform order crossover
    for route1, route2 in itertools.combinations(selected_routes, 2):
        crossover_point = random.randint(1, len(route1) - 1)
        child1 = route1[:crossover_point] + [city for city in route2 if city not in route1[:crossover_point]]
        child2 = route2[:crossover_point] + [city for city in route1 if city not in route2[:crossover_point]]
        offspring.extend([child1, child2])

    # Perform mutation
    for i in range(len(offspring)):
        if random.random() < 0.2:
            idx1, idx2 = random.sample(range(len(offspring[i])), 2)
            offspring[i][idx1], offspring[i][idx2] = offspring[i][idx2], offspring[i][idx1]
    
    return offspring

# Evaluate the population
def evaluate_population(population):
    return [(route, total_distance(route)) for route in population]

# Genetic algorithm
def genetic_algorithm(population_size, num_generations):
    population = generate_initial_population(population_size)
    best_route = None
    best_distance = float('inf')

    for gen in range(num_generations):
        logging.info(f"Generation {gen + 1}/{num_generations}")
        
        # Evaluate fitness of the entire population
        evaluation_start_time = time.time()
        logging.info("Evaluating fitness of population...")
        evaluated_population = evaluate_population(population)
        evaluation_end_time = time.time()
        evaluation_time = evaluation_end_time - evaluation_start_time
        logging.info(f"Sequential fitness evaluation finished in {evaluation_time:.2f} seconds")
        
        # Update population with evaluated routes
        population = [route for route, _ in evaluated_population]

        # Find the best route in the evaluated population
        for route, distance in evaluated_population:
            if distance < best_distance:
                best_distance = distance
                best_route = route

        logging.info(f"Best distance in generation {gen + 1}: {best_distance}")

        # Evolve the population
        population = evolve_population(population)

    logging.info("Genetic algorithm finished.")

    return best_route, best_distance

#def plot_route(best_route):
    plt.figure(figsize=(12, 8))
    m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
    m.drawcoastlines()
    m.drawcountries()

    for city in best_route:
        lat = cities[city][0]
        lon = cities[city][1]
        x, y = m(lon, lat)
        m.plot(x, y, 'ro', markersize=5)
        plt.text(x, y, city, fontsize=12, color='b', ha='right', va='bottom') # type: ignore

    for i in range(len(best_route) - 1):
        city1 = best_route[i]
        city2 = best_route[(i + 1)]
        lat1, lon1 = cities[city1]
        lat2, lon2 = cities[city2]
        x1, y1 = m(lon1, lat1)
        x2, y2 = m(lon2, lat2)
        #m.plot([x1, x2], [y1, y2], color='r', linewidth=1)
        plt.arrow(x1, y1, x2 - x1, y2 - y1, head_width=100000, head_length=100000, fc='b', ec='b') # type: ignore
        plt.text((x1 + x2) / 2, (y1 + y2) / 2, str(i + 1), fontsize=12, color='r') # type: ignore

    city1 = best_route[-1]
    city2 = best_route[0]
    lat1, lon1 = cities[city1]
    lat2, lon2 = cities[city2]
    x1, y1 = m(lon1, lat1)
    x2, y2 = m(lon2, lat2)
    plt.arrow(x1, y1, x2 - x1, y2 - y1, head_width=100000, head_length=100000, fc='b', ec='b') # type: ignore
    plt.text((x1 + x2) / 2, (y1 + y2) / 2, 7, fontsize=12, color='r') # type: ignore

    plt.title("Best Route")
    plt.show()

if __name__ == "__main__":
    setup_logger()
    logger = logger.PerformanceLogger()
    logger.start()
    best_route, best_distance = genetic_algorithm(population_size, num_generations)
    logging.info(f"Best Route: {best_route}")
    logging.info(f"Best Distance: {best_distance}")
    logs = logger.stop()
    #plot_route(best_route)
    # for log in logs:
    #     logging.info(log)