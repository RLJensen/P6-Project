FROM python:3.9.9

WORKDIR /whisperWorkload

ADD requirements.txt /whisperWorkload/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install git -y
RUN apt-get install -y ffmpeg

COPY whisperWorkload.py .
COPY models/base.pt .
COPY logger.py .
COPY files .

CMD ["python", "whisperWorkload.py"]
