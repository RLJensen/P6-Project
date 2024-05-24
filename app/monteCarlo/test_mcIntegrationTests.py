import unittest
from unittest.mock import patch
import logging
from io import StringIO
import random

# Assuming the functions are in a module named `dice_module`
from monteCarloAlgo import estimateDice

class TestEstimateDiceIntegration(unittest.TestCase):

    @patch('monteCarloAlgo.roll3Dice')
    @patch('monteCarloAlgo.logging.info')
    @patch('monteCarloAlgo.logging.error')
    def test_estimateDice_expected_funds(self, mock_logging_error, mock_logging_info, mock_roll3Dice):
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


    @patch('monteCarloAlgo.roll3Dice')
    @patch('monteCarloAlgo.logging.info')
    @patch('monteCarloAlgo.logging.error')
    def test_estimateDice_expected_return(self, mock_logging_error, mock_logging_info, mock_roll3Dice):
        # Mock roll3Dice to control its output
        mock_roll3Dice.side_effect = [16, 14, 13, 15, 18, 12, 11, 10, 15, 6]
        expected_return = [9800,4,[0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,2,1,0,1]]
        funds = 10000
        initial_wager = 100
        count = 10
        
        actual_return = estimateDice(funds, initial_wager, count)
        
        # Check that logging.info was called
        self.assertTrue(mock_logging_info.called)
        self.assertFalse(mock_logging_error.called)

        self.assertEqual(actual_return[0],expected_return[0])
        self.assertEqual(actual_return[1],expected_return[1])
        for i, logs in enumerate(actual_return[2]):
            self.assertEqual(logs,expected_return[2][i])

    @patch('monteCarloAlgo.roll3Dice')
    @patch('monteCarloAlgo.logging.info')
    @patch('monteCarloAlgo.logging.error')
    def test_estimateDice_expected_numWins(self, mock_logging_error, mock_logging_info, mock_roll3Dice):
        # Mock roll3Dice to control its output
        mock_roll3Dice.side_effect = [16, 14, 13, 15, 18, 12, 11, 10, 15, 6]

        funds = 10000
        initial_wager = 100
        count = 10
        
        final_funds, num_wins, rollLog = estimateDice(funds, initial_wager, count)
        
        # Check that logging.info was called
        self.assertTrue(mock_logging_info.called)
        self.assertFalse(mock_logging_error.called)

        self.assertEqual(num_wins, 4)



if __name__ == '__main__':
    unittest.main()