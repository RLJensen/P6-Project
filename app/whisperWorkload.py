import whisper
import logger
from googlesearch import search

def loadModel():
    logs = []
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    model = whisper.load_model("tiny")
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    result = model.transcribe("test.mp3",fp16=False)
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)

    whisperText = list(result.values())[0]
    searchresult = performSearch(whisperText)
    return result, logs, searchresult

def performSearch(query):
    result = search(query,10,"en",None,False,10,5)
    return result