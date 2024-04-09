import os
import random
import whisper
import logging
import logger
from googlesearch import search

def startWorkload():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting whisper workload")
    whisper = loadModel()
    whisperResult = whisper[0]
    whisperSearchResult = whisper[1]
    logging.info("Now starting Whisper workload")
    for key, value in whisperResult.items():
        print(key, ":", value)

    for info in whisperSearchResult:
        logging.info(info)

def loadModel():
    files = os.listdir(os.getcwd())
    sound_file = random.choice([file for file in files if file.endswith('.mp3')])
    model = whisper.load_model("base",None,download_root="./")
    result = model.transcribe(sound_file,fp16=False)

    whisperText = list(result.values())[0]
    searchresult = performSearch(whisperText)
    return result, searchresult

def performSearch(query):
    result = search(query,10,"en",None,False,10,5)
    return result

if __name__ == "__main__":
    logger = logger.PerformanceLogger()
    logger.start()
    startWorkload()
    logs = logger.stop()
    # for log in logs:
    #     logging.info(log)