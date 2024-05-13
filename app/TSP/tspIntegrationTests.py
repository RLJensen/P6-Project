import unittest
from unittest.mock import patch, mock_open
import os
from tspAlgorithm import read_city_coordinates, genetic_algorithm, setup_logger

class TestGeneticAlgorithmIntegration(unittest.TestCase):
    def setUp(self):
        # Mock environment variables
        self.patcher_env = patch.dict(os.environ, {
            'GRAFANACLOUD_URL': 'http://example.com',
            'GRAFANACLOUD_USERNAME': 'username',
            'GRAFANACLOUD_PASSWORD': 'password',
            'hostname': 'test_host'
        })
        self.patcher_env.start()

        # Mock city data
        self.mock_city_data = "City1,34.05,-118.25\nCity2,40.71,-74.00\nCity3,51.50,-0.12\n"
        self.mock_open = mock_open(read_data=self.mock_city_data)

        # Mock logging
        self.patcher_logger = patch('logging.getLogger')
        self.mock_logger = self.patcher_logger.start()

        setup_logger()  # Set up the logger

    def tearDown(self):
        self.patcher_env.stop()
        self.patcher_logger.stop()

    @patch('builtins.open', new_callable=mock_open, read_data="City1,34.05,-118.25\nCity2,40.71,-74.00\nCity3,51.50,-0.12\n")
    def test_genetic_algorithm_integration(self, mock_file):
        # Test read_city_coordinates function
        filename = 'mock_file.txt'
        cities = read_city_coordinates(filename, 3)
        expected_cities = {
            "City1": (34.05, -118.25),
            "City2": (40.71, -74.00),
            "City3": (51.50, -0.12)
        }
        self.assertEqual(cities, expected_cities)

        # Test genetic_algorithm function
        best_route, best_distance = genetic_algorithm(cities)
        # Check that the best_route contains all cities
        if best_route is not None:
            self.assertEqual(set(best_route), set(expected_cities.keys()))
        self.assertIsInstance(best_distance, float)

    def test_logger_setup(self):
        # Ensure the logger setup doesn't raise an error
        setup_logger()
        self.mock_logger.assert_called()

if __name__ == '__main__':
    unittest.main()


