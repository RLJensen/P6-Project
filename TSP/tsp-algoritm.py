from math import atan2, cos, radians, sin, sqrt
import numpy as np
import random
import itertools
import multiprocessing
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read city coordinates from file
def read_city_coordinates(filename):
    city_coordinates = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            city = parts[0]
            latitude = float(parts[1])
            longitude = float(parts[2])
            city_coordinates[city] = (latitude, longitude)
    return city_coordinates

# Select random cities
def select_random_cities(city_coordinates, num_cities):
    cities = random.sample(list(city_coordinates.keys()), num_cities)
    return {city: city_coordinates[city] for city in cities}

filename = 'cities.txt'
city_coordinates = read_city_coordinates(filename)

num_cities = 5  # Specify the number of cities you want to select
random_cities = select_random_cities(city_coordinates, num_cities)

# Example cities and their coordinates (latitude, longitude)
cities = {
    "Tokyo": (35.6839, 139.7744),
    "New York": (40.6943, -73.9249),
    "Mexico City": (19.4333, -99.1333),
    "Mumbai": (18.9667, 72.8333),
    "Sao Paulo": (-23.5504, -46.6339)
}

# Define parameters for the genetic algorithm
population_size = 10 # Number of routes in each generation
num_generations = 5 # Number of generations
num_cpus = 3 # Number of Workers

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

    for _ in range(num_generations):
        logging.info(f"Generation {_ + 1}/{num_generations}")
        # Split the population into subpopulations
        subpopulations = [population[i::num_cpus] for i in range(num_cpus)]

        evaluation_start_time = time.time()
        logging.info("Evaluating fitness of subpopulations...")

        # Evaluate fitness of subpopulations in parallel
        with multiprocessing.Pool(processes=num_cpus) as pool:
            evaluated_subpopulations = pool.map(evaluate_population, subpopulations)

        evaluation_end_time = time.time()
        evaluation_time = evaluation_end_time - evaluation_start_time
        logging.info(f"Parallel fitness evaluation finished in {evaluation_time:.2f} seconds")


        # Flatten the evaluated subpopulations
        population = [route for subpopulation in evaluated_subpopulations for route, _ in subpopulation]

        # Find the best route in the evaluated subpopulations
        for subpopulation in evaluated_subpopulations:
            for route, distance in subpopulation:
                if distance < best_distance:
                    best_distance = distance
                    best_route = route

        logging.info(f"Best distance in generation {_ + 1}: {best_distance}")

        # Evolve the population
        population = evolve_population(population)

    logging.info("Genetic algorithm finished.")

    return best_route, best_distance

if __name__ == "__main__":
    start_time = time.time()
    best_route, best_distance = genetic_algorithm(population_size, num_generations)
    end_time = time.time()
    print("Best Route:", best_route)
    print("Best Distance:", best_distance)
    print("Time taken:", end_time - start_time, "seconds")
