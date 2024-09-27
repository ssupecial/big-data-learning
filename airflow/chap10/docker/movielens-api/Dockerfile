FROM python:3.8-slim

RUN pip install pandas Flask click Flask-HTTPAuth

COPY app.py fetch_ratings.py /
RUN python /fetch_ratings.py --output_path /ratings.csv

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["/app.py"]