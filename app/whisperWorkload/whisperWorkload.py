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
                  "affinity":"worker3",
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
workload_type = "Whisper"
uuid = str(uuid.uuid4())
hostname = os.getenv('hostname', 'unknown')

def startWorkload():
    whisper = loadModel()
    whisperResult = whisper[0]
    whisperSearchResult = whisper[1]
    for key, value in whisperResult.items():
        print(key, ":", value)

    for info in whisperSearchResult:
        logging.info(info)

# Load the model and transcribe the sound file, if no sound file is found, raises an error
def loadModel():
    files = os.listdir(os.getcwd())
    sound_files = [file for file in files if file.endswith('.mp3')]

    if not sound_files:  # Check if the list is empty
        raise FileNotFoundError("No MP3 sound files found in the directory.")

    logging.info(f"Found {len(sound_files)} sound files: {sound_files}")
    sound_file = random.choice(sound_files)
    logging.info(f"Selected sound file: {sound_file}")
    model = whisper.load_model("tiny", None, download_root = "./")
    result = model.transcribe(sound_file, fp16 = False)

    whisperText = list(result.values())[0]
    searchresult = performSearch(whisperText)
    return result, searchresult

# Perform a google search on the transcribed text
def performSearch(query):
    result = search(query,5,"en",None,False,10,5)
    return result

if __name__ == "__main__":
    setup_logger()
    logger = logger.PerformanceLogger()
    logger.start()
    try:
        startWorkload()
        logger.stop()
    except FileNotFoundError as e:
        logging.error(str(e))
        logger.stop()