import unittest
import tspAlgorithm
from unittest.mock import patch, MagicMock
import os
import logging
from tspAlgorithm import setup_logger

class TestTSP(unittest.TestCase):

    cities = tspAlgorithm.read_city_coordinates('cities.txt', 5)

    def test_read_city_coordinates(self):
        filename = 'TSP/cities.txt'
        num_cities = 10
        cities = tspAlgorithm.read_city_coordinates(filename, num_cities)
        self.assertEqual(len(cities), num_cities)

    def test_generate_initial_population(self):
        population_size = 5
        population = tspAlgorithm.generate_initial_population(population_size, self.cities)
        self.assertEqual(len(population), population_size)
    
    def test_total_distance(self):
        cities = {'Tokyo': (35.6897,139.6922), 'Jakarta': (-6.175,106.8275), 'Manila': (14.5958,120.9772), 'Seoul': (37.56,126.99), 'Mexico City': (19.4333,-99.1333)}        
        route = ['Tokyo', 'Jakarta', 'Manila', 'Seoul', 'Mexico City']
        distance = tspAlgorithm.total_distance(route, cities)
        self.assertTrue(34000 < distance < 35000)
    
    def test_evolve_population(self):
        subpopulation = [['Manila', 'Tokyo', 'Seoul', 'Jakarta', 'Mexico City'],
                         ['Tokyo', 'Jakarta', 'Seoul', 'Manila', 'Mexico City'],
                         ['Tokyo', 'Mexico City', 'Seoul', 'Manila', 'Jakarta'],
                         ['Tokyo', 'Manila', 'Mexico City', 'Jakarta', 'Seoul'],
                         ['Jakarta', 'Mexico City', 'Tokyo', 'Seoul', 'Manila'],
                         ['Seoul', 'Tokyo', 'Jakarta', 'Mexico City', 'Manila'], 
                         ['Seoul', 'Mexico City', 'Manila', 'Jakarta', 'Tokyo'], 
                         ['Seoul', 'Manila', 'Mexico City', 'Tokyo', 'Jakarta'], 
                         ['Tokyo', 'Seoul', 'Jakarta', 'Mexico City', 'Manila'], 
                         ['Jakarta', 'Tokyo', 'Seoul', 'Mexico City', 'Manila']]
        offspring = tspAlgorithm.evolve_population(subpopulation)
        self.assertEqual(len(offspring), 20)
    
    def test_evaluate_population(self):
        cities = {'Tokyo': (35.6897,139.6922), 'Jakarta': (-6.175,106.8275), 'Manila': (14.5958,120.9772), 'Seoul': (37.56,126.99), 'Mexico City': (19.4333,-99.1333)}        

        population = [['Manila', 'Tokyo', 'Seoul', 'Jakarta', 'Mexico City'], 
                      ['Tokyo', 'Jakarta', 'Seoul', 'Manila', 'Mexico City'], 
                      ['Tokyo', 'Mexico City', 'Seoul', 'Manila', 'Jakarta'], 
                      ['Tokyo', 'Manila', 'Mexico City', 'Jakarta', 'Seoul'], 
                      ['Jakarta', 'Mexico City', 'Tokyo', 'Seoul', 'Manila']]
        evaluated_population = tspAlgorithm.evaluate_population(population, cities)
        self.assertEqual(len(evaluated_population), 5)
        self.assertEqual(len(evaluated_population[0]), 2)
    
    def test_genetic_algorithm(self):
        population_size = 10
        num_generations = 3
        result = tspAlgorithm.genetic_algorithm(self.cities)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
