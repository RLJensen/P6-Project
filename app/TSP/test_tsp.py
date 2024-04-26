import unittest
import tspAlgorithm

class TestTSP(unittest.TestCase):

    cities = tspAlgorithm.read_city_coordinates('cities.txt', 10)

    def test_read_city_coordinates(self):
        filename = 'cities.txt'
        num_cities = 10
        cities = tspAlgorithm.read_city_coordinates(filename, num_cities)
        self.assertEqual(len(cities), num_cities)

    def test_generate_initial_population(self):
        population_size = 5
        population = tspAlgorithm.generate_initial_population(population_size, self.cities)
        self.assertEqual(len(population), population_size)
    
    def test_total_distance(self):
        route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        distance = tspAlgorithm.total_distance(route, self.cities)
        self.assertEqual(distance, 9)
    
    def test_evolve_population(self):
        subpopulation = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        offspring = tspAlgorithm.evolve_population(subpopulation)
        self.assertEqual(len(offspring), 10)
    
    def test_evaluate_population(self):
        population = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(10)]
        evaluated_population = tspAlgorithm.evaluate_population(population, self.cities)
        self.assertEqual(len(evaluated_population), 10)
        self.assertEqual(len(evaluated_population[0]), 2)
    
    def test_genetic_algorithm(self):
        population_size = 10
        num_generations = 3
        tspAlgorithm.genetic_algorithm(self.cities)
        self.assertTrue(True)
    
if __name__ == '__main__':
    unittest.main()
