import random
import logger
import logging

def startWorkload():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting program")

    logObjects = estimateDice(10000,100,100)

    for obj in logObjects:
        logging.info(obj)

def estimateDice(funds,initial_wager,wager_count):
    logs = []
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    value = funds
    wager = initial_wager

    currentWager = 0

    while currentWager < wager_count:
        currentLog = logger.getCPUandRAMLoad(logger.getLoad())
        logs.append(currentLog)
        if rollDice():
            value += wager
        else:
            value -= wager

        currentWager += 1
        print('Funds:', value)
        currentLog = logger.getCPUandRAMLoad(logger.getLoad())
        logs.append(currentLog)
    return logs
    
def rollDice():
    roll = random.randint(1,100)

    if roll == 100:
        print(roll,'roll was 100, you lose. What are the odds?! Play again!')
        return False
    elif roll <= 50:
        print(roll,'roll was 1-50, you lose.')
        return False
    elif 100 > roll >= 50:
        print(roll,'roll was 51-99, you win! *pretty lights flash* (play more!)')
        return True
    
if __name__ == "__monteCarloAlgo__":
    startWorkload()