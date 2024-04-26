import os
import random
import whisper
import logging
import logger
from googlesearch import search
import uuid
import socket

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.hostname = hostname
        record.workload_type = workload_type
        record.uuid = uuid
        return super().format(record)

def setup_logger():
    custom_logger = logging.getLogger()
    custom_logger.setLevel(logging.INFO)

    if custom_logger.hasHandlers():
        custom_logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(hostname)s - %(workload_type)s - %(uuid)s - %(message)s')
    handler.setFormatter(formatter)

    custom_logger.addHandler(handler)

workload_type = "Whisper"
uuid = str(uuid.uuid4())
hostname = socket.gethostname()

def startWorkload():
    whisper = loadModel()
    if(whisper == None):
        logging.info("Failed to load model")
        return
    whisperResult = whisper[0]
    whisperSearchResult = whisper[1]
    for key, value in whisperResult.items():
        print(key, ":", value)

    for info in whisperSearchResult:
        logging.info(info)

def loadModel():
    files = os.listdir(os.getcwd())
    sound_file = random.choice([file for file in files if file.endswith('.mp3')])
    if(sound_file == None):
        logging.info("No sound files found")
        return None

    model = whisper.load_model("small",None,download_root="./")
    result = model.transcribe(sound_file,fp16=False)

    whisperText = list(result.values())[0]
    searchresult = performSearch(whisperText)
    return result, searchresult

def performSearch(query):
    result = search(query,5,"en",None,False,10,5)
    return result

if __name__ == "__main__":
    setup_logger()
    logger = logger.PerformanceLogger()
    logger.start()
    startWorkload()
    logs = logger.stop()
    # for log in logs:
    #     logging.info(log)