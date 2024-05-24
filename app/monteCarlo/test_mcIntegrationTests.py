import unittest
from unittest.mock import patch
import logging
from io import StringIO
import random

# Assuming the functions are in a module named `dice_module`
from monteCarloAlgo import estimateDice, doRolls, roll3Dice

class TestEstimateDiceIntegration(unittest.TestCase):

    @patch('monteCarloAlgo.roll3Dice')
    @patch('monteCarloAlgo.logging.info')
    @patch('monteCarloAlgo.logging.error')
    def test_estimateDice(self, mock_logging_error, mock_logging_info, mock_roll3Dice):
        # Mock roll3Dice to control its output
        mock_roll3Dice.side_effect = [16, 14, 13, 15, 18, 12, 11, 10, 15, 6]

        funds = 10000
        initial_wager = 100
        count = 10
        
        final_funds, num_wins, rollLog = estimateDice(funds, initial_wager, count)
        
        # Check that logging.info was called
        self.assertTrue(mock_logging_info.called)
        self.assertFalse(mock_logging_error.called)
        
        # Check the final values
        expected_funds = 10000 + 100*4 - 100*6  # 3 wins (16, 15, 15), 7 losses
        self.assertEqual(final_funds, expected_funds)
        self.assertEqual(num_wins, 4)
        self.assertEqual(rollLog[16], 1)
        self.assertEqual(rollLog[14], 1)
        self.assertEqual(rollLog[13], 1)
        self.assertEqual(rollLog[15], 2)
        self.assertEqual(rollLog[18], 1)
        self.assertEqual(rollLog[12], 1)
        self.assertEqual(rollLog[11], 1)
        self.assertEqual(rollLog[10], 1)
        self.assertEqual(rollLog[6], 1)
        self.assertEqual(sum(rollLog), count)

        # Ensure the correct log messages were generated
        log_output = [call[0][0] for call in mock_logging_info.call_args_list]
        self.assertIn("Wager count: 10", log_output)
        self.assertIn("Wager: 100", log_output)
        self.assertIn("Initial funds: 10000", log_output)
        self.assertIn(f"Number of wins: {num_wins}", log_output)
        self.assertIn(f"Number of losses: {count - num_wins}", log_output)
        self.assertIn(f"Final funds: {final_funds}", log_output)

        # Check percentage logs for each roll result
        percentage_logs = [
            f"estimate of {i} happens {round(rollLog[i] / count * 100, 5)}% of the time"
            for i in range(19) if i > 2 and rollLog[i] > 0
        ]
        for log in percentage_logs:
            self.assertIn(log, log_output)

if __name__ == '__main__':
    unittest.main()