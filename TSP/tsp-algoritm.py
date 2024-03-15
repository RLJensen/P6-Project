import numpy as np
import random
import itertools
import multiprocessing
import time

# Example city coordinates
cities = {
    "A": (0, 0),
    "B": (1, 2),
    "C": (3, 1),
    "D": (5, 3),
    "E": (4, 0)
}

# Define parameters for the genetic algorithm
population_size = 1
num_generations = 1
num_cpus = 3

# Calculate distance between two cities
def distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Calculate total distance of a route
def total_distance(route):
    total = 0
    for i in range(len(route) - 1):
        total += distance(cities[route[i]], cities[route[i+1]])
    total += distance(cities[route[-1]], cities[route[0]])
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
        # Split the population into subpopulations
        subpopulations = [population[i::num_cpus] for i in range(num_cpus)]

        # Evaluate fitness of subpopulations in parallel
        with multiprocessing.Pool(processes=num_cpus) as pool:
            evaluated_subpopulations = pool.map(evaluate_population, subpopulations)

        # Flatten the evaluated subpopulations
        population = [route for subpopulation in evaluated_subpopulations for route, _ in subpopulation]

        # Find the best route in the evaluated subpopulations
        for subpopulation in evaluated_subpopulations:
            for route, distance in subpopulation:
                if distance < best_distance:
                    best_distance = distance
                    best_route = route

        # Evolve the population
        population = evolve_population(population)

    return best_route, best_distance

if __name__ == "__main__":
    start_time = time.time()
    best_route, best_distance = genetic_algorithm(population_size, num_generations)
    end_time = time.time()
    print("Best Route:", best_route)
    print("Best Distance:", best_distance)
    print("Time taken:", end_time - start_time, "seconds")
