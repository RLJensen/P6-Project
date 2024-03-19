import logging
import psutil
from datetime import datetime

def getLoad():
    CPULoad = psutil.cpu_times_percent() #psutil.cpu_percent(interval=None)
    RAMLoad = psutil.virtual_memory().percent
    availableRAM = psutil.virtual_memory().available
    totalLoad = [CPULoad, RAMLoad, availableRAM]
    return totalLoad

class getCPUandRAMLoad:
    def __init__(self,getLoad=None):
        self.currentTime = datetime.now()
        self.formattedTime = self.currentTime.strftime("%d-%m-%Y %H:%M:%S")
        self.loadData = getLoad
        
        if len(self.loadData) != 3:
            logging.error("Could not get CPU and RAM information", self.formattedTime)

    def __str__(self):
        return f"CPU and RAM Load Data at {self.formattedTime}: CPU: {self.loadData[0]}% RAM: {self.loadData[1]}% Available RAM:{self.loadData[2]/1000000000}GB"


                


