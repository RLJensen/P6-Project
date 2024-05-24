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
        print(cities)
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
    
    @patch('tspAlgorithm.logging.getLogger')
    @patch('tspAlgorithm.load_dotenv')
    @patch('tspAlgorithm.logging_loki.LokiHandler')
    @patch('tspAlgorithm.hostname', 'mock-hostname')
    @patch('tspAlgorithm.workload_type', 'mock-workload')
    @patch('tspAlgorithm.uuid', 'mock-uuid')
    def test_setup_logger(self, mock_LokiHandler, mock_load_dotenv, mock_getLogger):
        # Mock the environment variables
        mock_env = {
            'GRAFANACLOUD_URL': 'http://mock-url',
            'GRAFANACLOUD_USERNAME': 'mock-user',
            'GRAFANACLOUD_PASSWORD': 'mock-pass'
        }
        
        with patch.dict(os.environ, mock_env):
            # Mock the logger and its methods
            mock_logger = MagicMock()
            mock_getLogger.return_value = mock_logger

            # Mock the LokiHandler instance
            mock_handler = MagicMock()
            mock_LokiHandler.return_value = mock_handler

            # Call the setup_logger function
            setup_logger()

            # Check logger level is set to INFO
            mock_logger.setLevel.assert_called_with(logging.INFO)

            # Ensure load_dotenv was called
            mock_load_dotenv.assert_called_once()

            # Check if existing handlers were cleared
            mock_logger.handlers.clear.assert_called_once()

            # Check LokiHandler was created with correct parameters
            mock_LokiHandler.assert_called_once_with(
                url='http://mock-url',
                tags={
                    "application": "Workload",
                    "host": 'mock-hostname',
                    "workload":'mock-workload',
                    "affinity": "worker3",
                    "uuid": 'mock-uuid'
                },
                auth=('mock-user', 'mock-pass'),
                version="1"
            )

            # Check the handler was added to the logger
            mock_logger.addHandler.assert_called_once_with(mock_handler)

            # Verify formatter was set correctly
            mock_handler.setFormatter.assert_called_once()
            formatter_arg = mock_handler.setFormatter.call_args[0][0]
            self.assertIsInstance(formatter_arg, logging.Formatter)
            self.assertEqual(formatter_arg._fmt, '%(asctime)s - %(levelname)s - %(message)s')

    @patch('tspAlgorithm.logging.getLogger')
    @patch('tspAlgorithm.load_dotenv')
    @patch('tspAlgorithm.logging_loki.LokiHandler', side_effect=Exception('mock error'))
    def test_setup_logger_exception(self, mock_LokiHandler, mock_load_dotenv, mock_getLogger):
        # Mock the environment variables
        mock_env = {
            'GRAFANACLOUD_URL': 'http://mock-url',
            'GRAFANACLOUD_USERNAME': 'mock-user',
            'GRAFANACLOUD_PASSWORD': 'mock-pass'
        }

        with patch.dict(os.environ, mock_env):
            # Mock the logger and its methods
            mock_logger = MagicMock()
            mock_getLogger.return_value = mock_logger

            # Expect the setup_logger to raise an exception
            with self.assertRaises(Exception) as context:
                setup_logger()

            self.assertEqual(str(context.exception), 'mock error')

if __name__ == '__main__':
    unittest.main()
