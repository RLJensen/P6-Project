import logging
import psutil
import threading
import time

# Get CPU and RAM load
def getLoad():
    CPULoad = psutil.cpu_percent()
    RAMLoad = psutil.virtual_memory().percent
    availableRAM = psutil.virtual_memory().available
    totalLoad = [CPULoad, RAMLoad, availableRAM]
    return totalLoad

class PerformanceLogger:
    def __init__(self):
        self._running = False
        self._thread = None
        self.timer = 0
    
    # Start the workload with a new thread
    def start(self):
        self._running = True
        logging.info(f"Starting Workload")
        self.timer = time.time()
        self._thread = threading.Thread(target=self.update)
        self._thread.start()

    # Stop the workload and join the thread
    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
        elapsedTime = time.time() - self.timer
        logging.info(f"Workload Finished in {elapsedTime} seconds")
    
    # Update the logger with CPU and RAM load, will create a log every 0.2 seconds
    def update(self):
        while self._running:
            self.loadData = getLoad()
            logging.info(f"CPU: {self.loadData[0]}% RAM: {self.loadData[1]}% Available RAM: {round(self.loadData[2]/1000000000,2)} GB", 
                         extra={"tags":
                             {"CPU":f"{self.loadData[0]}%", 
                              "RAM":f"{self.loadData[1]}%",
                              "Available RAM":f"{round(self.loadData[2]/1000000000,2)} GB"
                              }})
            time.sleep(0.2)