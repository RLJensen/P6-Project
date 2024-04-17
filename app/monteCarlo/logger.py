import logging
import psutil
from datetime import datetime
import threading
import time
import uuid
import socket

def getLoad():
    CPULoad = psutil.cpu_percent() #psutil.cpu_percent(interval=None)
    RAMLoad = psutil.virtual_memory().percent
    availableRAM = psutil.virtual_memory().available
    totalLoad = [CPULoad, RAMLoad, availableRAM]
    return totalLoad

class PerformanceLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logs = []
        self._running = False
        self._thread = None
    
    def start(self):
        self._running = True
        logging.info("Starting program")
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        logging.info(f"Hostname: {hostname}")
        logging.info(f"IP Address: {ip_address}")
        logging.info(f"MAC Address: {mac_address}")
        self._thread = threading.Thread(target=self.update)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
        return self.logs
    
    def update(self):
        while self._running:
            self.loadData = getLoad()
            self.formattedTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")[:-3]
            logging.info(f"CPU and RAM Load Data at {self.formattedTime}: CPU: {self.loadData[0]}% RAM: {self.loadData[1]}% Available RAM:{round(self.loadData[2]/1000000000,2)} GB")
            # self.logs.append(currentLog)
            time.sleep(0.2)