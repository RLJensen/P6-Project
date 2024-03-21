import whisper
import logger

def loadModel():
    logs = []
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    model = whisper.load_model("tiny")
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    result = model.transcribe("recording.mp3",fp16=False)
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    logs.append(currentLog)
    return result, logs