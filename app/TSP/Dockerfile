FROM python:3.9.9

WORKDIR /TSP

ADD requirements.txt /TSP/requirements.txt
RUN pip install -r requirements.txt

COPY tsp-algorithm.py .
COPY logger.py .
COPY cities.txt .

CMD ["python", "tsp-algorithm.py"]