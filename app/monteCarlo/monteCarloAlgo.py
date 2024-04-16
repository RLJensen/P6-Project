import random
import logging
import logger

def startWorkload():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting program")
    count = random.randint(1000000,5000000)

    estimateDice(10000, 100, count)

def estimateDice(funds,initial_wager,wager_count):
    value = funds
    wager = initial_wager
    num_wins = 0
    logging.info(f"Wager count: {wager_count}")
    logging.info(f"Wager: {wager}")
    logging.info(f"Initial funds: {value}")

    currentWager = 0

    while currentWager < wager_count:
        if rollDice():
            value += wager
            num_wins += 1
        else:
            value -= wager

        currentWager += 1
    logging.info(f"Number of wins: {num_wins}")
    logging.info(f"Number of losses: {wager_count - num_wins}")
    logging.info(f"Final funds: {value}")

    
def rollDice():
    roll = random.randint(1,100)

    if roll == 100:
        # print(roll,'roll was 100, you lose. What are the odds?! Play again!')
        return False
    elif roll <= 50:
        # print(roll,'roll was 1-50, you lose.')
        return False
    elif 100 > roll >= 50:
        # print(roll,'roll was 51-99, you win! *pretty lights flash* (play more!)')
        return True
    
if __name__ == "__main__":
    logger = logger.PerformanceLogger()
    logger.start()
    startWorkload()
    logs = logger.stop()
    # for log in logs:
    #     logging.info(log)