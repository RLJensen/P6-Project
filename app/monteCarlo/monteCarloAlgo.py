import random
import logging
import logger
import uuid
import socket
import logging_loki
import os
from dotenv import load_dotenv

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.hostname = hostname
        record.workload_type = workload_type
        record.uuid = uuid
        return super().format(record)

def setup_logger():
    custom_logger = logging.getLogger()
    custom_logger.setLevel(logging.INFO)
    
    load_dotenv()

    if custom_logger.hasHandlers():
        custom_logger.handlers.clear()

    try:
        handler = logging_loki.LokiHandler(
            url=os.environ['GRAFANACLOUD_URL'],  # Directly accessing for immediate error on misconfig
            tags={"application": "Workload",
                  "host": hostname,
                  "workload": workload_type,
                  "uuid": uuid},
            auth=(os.environ['GRAFANACLOUD_USERNAME'], os.environ['GRAFANACLOUD_PASSWORD']),
            version="1",
        )
    except Exception as e:
        print(f"Failed to setup Loki handler: {str(e)}")  # Immediate feedback on failure
        raise
    
    formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(hostname)s - %(workload_type)s - %(uuid)s - %(message)s')
    handler.setFormatter(formatter)

    custom_logger.addHandler(handler)

workload_type = "Monte Carlo"
uuid = str(uuid.uuid4())
hostname = socket.gethostname()

def startWorkload():
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
    logger.stop()