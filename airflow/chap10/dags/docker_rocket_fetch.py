from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from airflow import DAG
import datetime as dt
import os


with DAG(
    dag_id="docker-operator-test",
    description="Fetches data from the Rocket API using Docker.",
    start_date=dt.datetime(2024, 9, 24),
    schedule_interval="@daily",
    catchup=False
) as dag:
    fetch_rockets = DockerOperator(
        task_id="fetch_rockets",
        image="ssupecial-airflow/rocket-fetch",
        command=[
            "fetch-rocket",
            "--start_date",
            "{{ds}}",
        ],
        network_mode="bridge", # or airflow
        container_name="fetch-rocket-da-{{ds}}",
        auto_remove="force",
        # Note: this host path is on the HOST, not in the Airflow docker container.
        mounts=[Mount(source="/Users/admin/Desktop/data", target="/data", type="bind")],
    )
    

    fetch_rockets 
