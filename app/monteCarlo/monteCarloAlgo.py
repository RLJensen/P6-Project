import random
import logging
import logger
import uuid
import socket

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.hostname = hostname
        record.uuid = uuid
        return super().format(record)

def setup_logger():
    custom_logger = logging.getLogger()
    custom_logger.setLevel(logging.INFO)

    if custom_logger.hasHandlers():
        custom_logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(hostname)s - %(uuid)s - %(message)s')
    handler.setFormatter(formatter)

    custom_logger.addHandler(handler)

uuid = str(uuid.uuid4())
hostname = socket.gethostname()

def startWorkload():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
    setup_logger()
    logger = logger.PerformanceLogger()
    logger.start()
    startWorkload()
    logs = logger.stop()
    # for log in logs:
    #     logging.info(log)