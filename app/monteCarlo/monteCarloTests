import unittest
from unittest.mock import patch
import logging
import monteCarloAlgo

class TestMonteCarlo(unittest.TestCase):
    @patch('monteCarloAlgo.random.randint')
    def test_estimateDice(self, mock_randint):
        mock_randint.return_value = 100  # Ensuring a predictable result for the rollDice function
        logging.disable(logging.CRITICAL)  # Disable logging to avoid cluttering the test output

        funds = 100
        initial_wager = 10
        wager_count = 5

        final_value, num_wins = monteCarloAlgo.estimateDice(funds, initial_wager, wager_count)

        # Assert that the final funds are equal to the initial funds minus (initial wager * wager count)
        self.assertEqual(final_value, funds - (initial_wager * wager_count))

        # Assert that the number of wins and losses are within expected ranges
        expected_wins = sum(1 for _ in range(wager_count) if monteCarloAlgo.rollDice())
        expected_losses = wager_count - expected_wins
        self.assertEqual(num_wins, expected_wins)
        self.assertEqual(wager_count - num_wins, expected_losses)

    @patch('monteCarloAlgo.random.randint')
    def test_rollDice(self, mock_randint):
        # Test rollDice function with different roll values
        mock_randint.side_effect = [100, 25, 75]  # Mocking different roll values for testing

        # Test scenarios for each possible outcome
        self.assertFalse(monteCarloAlgo.rollDice())  # Test when roll is 100
        self.assertFalse(monteCarloAlgo.rollDice())  # Test when roll is between 1-50
        self.assertTrue(monteCarloAlgo.rollDice())   # Test when roll is between 51-99

if __name__ == '__main__':
    unittest.main()