FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

RUN pip install --upgrade pip

WORKDIR /app
COPY python_version/map.py /app/
COPY python_version/reduce.py /app/
COPY data/temperature_sample.txt /app/sample.txt

CMD ["sh", "-c", "cat /app/sample.txt | python map.py | sort | python reduce.py"]