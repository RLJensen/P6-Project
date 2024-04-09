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
    whisperLoad = whisper[1]
    whisperSearchResult = whisper[2]
    logging.info("Now starting Whisper workload")
    for key, value in whisperResult.items():
        print(key, ":", value)
    
    for info in whisperLoad:
        logging.info(info)

    for info in whisperSearchResult:
        logging.info(info)

def loadModel():
    files = os.listdir(os.getcwd())
    sound_file = random.choice([file for file in files if file.endswith('.mp3')])
    logs = []
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    model = whisper.load_model("base",None,download_root="./")
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    result = model.transcribe(sound_file,fp16=False)
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)

    whisperText = list(result.values())[0]
    searchresult = performSearch(whisperText)
    return result, logs, searchresult

def performSearch(query):
    result = search(query,10,"en",None,False,10,5)
    return result

if __name__ == "__main__":
    startWorkload()