import random
import logging
import logger
import uuid
import logging_loki
import os
from dotenv import load_dotenv

# Setup logger with Loki handler
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
                  "affinity":"worker2",
                  "uuid": uuid},
            auth=(os.environ['GRAFANACLOUD_USERNAME'], os.environ['GRAFANACLOUD_PASSWORD']),
            version="1",
        )
    except Exception as e:
        print(f"Failed to setup Loki handler: {str(e)}")  # Immediate feedback on failure
        raise
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    custom_logger.addHandler(handler)

# Information about workload, hostname and uuid
workload_type = "Monte Carlo"
uuid = str(uuid.uuid4())
hostname = os.environ['hostname']

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

    return value, num_wins
    
def rollDice():
    roll = random.randint(1,100)

    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll > 50:
        return True
    
if __name__ == "__main__":
    setup_logger()
    logger = logger.PerformanceLogger()
    logger.start()
    startWorkload()
    logger.stop()