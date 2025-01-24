FROM python:3.13

RUN apt-get install wget
RUN pip install pandas psycopg2 sqlalchemy

WORKDIR /app
COPY ingest_data.py .

ENTRYPOINT [ "python", "ingest_data.py" ]
