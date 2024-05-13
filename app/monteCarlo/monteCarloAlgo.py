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
hostname = os.getenv('hostname', 'unknown')

def startWorkload():
    count = random.randint(1000000,5000000)
    estimateDice(10000, 100, count)

def estimateDice(funds,initial_wager,count):
    value = funds
    wager = initial_wager
    num_wins = 0
    logging.info(f"Wager count: {count}")
    logging.info(f"Wager: {wager}")
    logging.info(f"Initial funds: {value}")
    try:
        rollLog = [0] * 19

        for r in range(count):
            rollresult = roll3Dice()
            rollLog[rollresult] += 1
            if rollresult >= 15:
                num_wins += 1
                value += wager
            else:
                value -= wager
            
    except Exception as e:
        logging.error(f"Error: {e}")

    logging.info(f"Number of wins: {num_wins}")
    logging.info(f"Number of losses: {count - num_wins}")
    logging.info(f"Final funds: {value}")
    for i, value in enumerate(rollLog):
        if i > 2:
            logging.info(f"estimate of {i} happpens {round(value / count * 100, 5)}% of the time")
        
def rollDice():
    return random.randint(1,6)

def roll3Dice():
    return rollDice() + rollDice() + rollDice()
    
if __name__ == "__main__":
    setup_logger()
    name = logger.PerformanceLogger()
    name.start()
    startWorkload()
    name.stop()

