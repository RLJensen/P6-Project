import whisper
import logging
import logger
from googlesearch import search

def startWorkload():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting whisper workload")
    loadModel()

def loadModel():
    logs = []
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    model = whisper.load_model("tiny",None,download_root="/models")
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    result = model.transcribe("whisperWorkload/test.mp3",fp16=False)
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)

    whisperText = list(result.values())[0]
    searchresult = performSearch(whisperText)
    return result, logs, searchresult

def performSearch(query):
    result = search(query,10,"en",None,False,10,5)
    return result

if __name__ == "__whisperWorkload__":
    startWorkload()