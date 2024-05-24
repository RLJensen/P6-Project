import unittest
import monteCarloAlgo as mca

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

if __name__ == '__main__':
    unittest.main()