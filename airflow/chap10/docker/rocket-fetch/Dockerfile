FROM python:3.8-slim

RUN pip install click pandas requests

COPY scripts/fetch.py /usr/local/bin/fetch-rocket
RUN chmod +x /usr/local/bin/fetch-rocket

ENV PATH="/usr/local/bin:${PATH}"