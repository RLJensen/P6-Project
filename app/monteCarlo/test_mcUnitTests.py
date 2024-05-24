import unittest
import monteCarloAlgo as mca
from unittest.mock import patch, MagicMock
import os
import logging
from monteCarloAlgo import setup_logger

class TestMonteCarloAlgo(unittest.TestCase):
    def test_rollDice(self):
        result = mca.rollDice()
        self.assertTrue(1 <= result <= 6)

    def test_roll3Dice(self):
        result = mca.roll3Dice()
        self.assertTrue(3 <= result <= 18)

    def test_estimateDice(self):
        funds = 10000
        initial_wager = 100
        count = 1000
        value, num_wins, rollLog = mca.estimateDice(funds, initial_wager, count)
        self.assertTrue(0 <= num_wins <= count)
        self.assertTrue(len(rollLog) == 19)

    def test_doRolls(self):
        rollLog = [0] * 19
        count = 1000
        num_wins = 0
        value = 10000
        wager = 100
        value, num_wins, rollLog = mca.doRolls(rollLog, count, num_wins, value, wager)
        self.assertTrue(0 <= num_wins <= count)
        self.assertTrue(len(rollLog) == 19)

    def test_convertToPercentage(self):
        rollLog = [0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 2, 0, 1, 2, 0, 0, 0]
        count = 10
        result = mca.convertToPercentage(rollLog, count)
        self.assertTrue(len(result) == 19)
        self.assertTrue(result[12] == 20)

    def test_startWorkload(self):
        result = mca.startWorkload()
        self.assertTrue(1000000 <= result <= 5000000)

    @patch('monteCarloAlgo.logging.getLogger')
    @patch('monteCarloAlgo.load_dotenv')
    @patch('monteCarloAlgo.logging_loki.LokiHandler')
    @patch('monteCarloAlgo.hostname', 'mock-hostname')
    @patch('monteCarloAlgo.workload_type', 'mock-workload')
    @patch('monteCarloAlgo.uuid', 'mock-uuid')
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

    @patch('monteCarloAlgo.logging.getLogger')
    @patch('monteCarloAlgo.load_dotenv')
    @patch('monteCarloAlgo.logging_loki.LokiHandler', side_effect=Exception('mock error'))
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