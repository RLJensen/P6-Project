FROM python:3.9.9

WORKDIR /acceptanceTest

ADD requirements.txt /acceptanceTest/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install git -y

COPY acceptanceTest.py .
COPY test.json .

CMD [ "python", acceptanceTest.py ]