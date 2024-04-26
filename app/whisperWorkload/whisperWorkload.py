import os
import random
import whisper
import logging
import logger
from googlesearch import search
import uuid
import socket
import logging_loki
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
    
    formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    custom_logger.addHandler(handler)

workload_type = "Whisper"
uuid = str(uuid.uuid4())
hostname = socket.gethostname()

def startWorkload():
    whisper = loadModel()
    whisperResult = whisper[0]
    whisperSearchResult = whisper[1]
    for key, value in whisperResult.items():
        print(key, ":", value)

    for info in whisperSearchResult:
        logging.info(info)

def loadModel():
    files = os.listdir(os.getcwd())
    sound_file = random.choice([file for file in files if file.endswith('.mp3')])
    model = whisper.load_model("tiny",None,download_root="./")
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
    logger.stop()