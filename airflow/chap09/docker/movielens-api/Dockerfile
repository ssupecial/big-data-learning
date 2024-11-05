FROM python:3.8-slim

RUN pip install fastapi uvicorn werkzeug pandas click
COPY app.py fetch_data.py /
RUN python /fetch_data.py --output_path /ratings.csv

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD ["/app.py"]