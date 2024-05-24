import unittest
from unittest.mock import patch
import monteCarloAlgo

class TestMonteCarloIntegration(unittest.TestCase):
    @patch('monteCarloAlgo.random.randint')
    def test_monteCarloWorkflow(self, mock_randint):
        # Mock the random number generator to create predictable results
        # Example pattern: [100, 25, 75, 60, 40] will dictate the behavior of rollDice
        mock_randint.side_effect = [100, 25, 75, 60, 40]  # Predictable pattern of results

        # Set up initial conditions for the simulation
        funds = 100
        initial_wager = 10
        wager_count = 5
        
        # Run the simulation with mocked randint behavior
        final_value, num_wins = monteCarloAlgo.estimateDice(funds, initial_wager, wager_count)

        # Define expected values based on the side effect:
        # rollDice results:
        # - 100 (loss)
        # - 25 (loss)
        # - 75 (win)
        # - 60 (win)
        # - 40 (loss)

        # Calculate the expected number of wins and losses
        expected_wins = 2
        expected_losses = wager_count - expected_wins

        # Calculate expected final value:
        # Starting with the initial funds and applying wins/losses
        expected_final_value = funds - (expected_losses * initial_wager) + (expected_wins * initial_wager)

        # Validate final fund value after simulation
        self.assertEqual(final_value, expected_final_value)

        # Verify the correct number of wins
        self.assertEqual(num_wins, expected_wins)

if __name__ == '__main__':
    unittest.main()