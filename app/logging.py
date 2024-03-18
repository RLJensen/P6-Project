import logging
import psutil


def monteCarloLogger():
    logging.basicConfig(filename="app.log", 
                        level=logging.INFO, 
                        format='%(asctime)s - CPU load: %(cpu_load)s - RAM load: %(ram_load)s - Used RAM: %(used_ram)s- %(message)s'
                        )
    
def getCPUandRAMLoad():
    CPULoad = psutil.cpu_percent()
    RAMLoad = psutil.virtual_memory().percent
    availableRAM = psutil.virtual_memory().available
    totalLoad = [CPULoad, RAMLoad, availableRAM]
    return totalLoad
