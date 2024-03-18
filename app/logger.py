import logging
import psutil
from datetime import datetime

def monteCarloLogger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
                        )

    
def getLoad():
    CPULoad = psutil.cpu_percent()
    RAMLoad = psutil.virtual_memory().percent
    availableRAM = psutil.virtual_memory().available
    totalLoad = [CPULoad, RAMLoad, availableRAM]
    return totalLoad

class getCPUandRAMLoad:
    def __init__(self,getLoad=None):
        currentTime = datetime.now()
        formattedTime = currentTime.strftime("%d-%m-%Y %H:%M:%S")

        if getLoad:
            data = self.getLoad
            if len(data) != 3:
                logging.error("Could not get CPU and RAM information")
            else:
                totalLoad = [data[0], data[1], data[2]]
                logging.info("Total CPU and RAM information has been fetched, time:", formattedTime)


