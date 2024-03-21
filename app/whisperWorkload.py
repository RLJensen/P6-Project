import whisper
import logger

def loadModel():
    currentLog = logger.getCPUandRAMLoad(logger.getLoad())
    model = whisper.load_model("tiny")
    currentLog += logger.getCPUandRAMLoad(logger.getLoad())
    result = model.transcribe("recording.mp3")
    currentLog += logger.getCPUandRAMLoad(logger.getLoad())
    return result, currentLog