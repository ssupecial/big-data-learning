from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount
from airflow import DAG
import datetime as dt
import os


with DAG(
    dag_id="docker-operator",
    description="Fetches ratings from the Movielens API using Docker.",
    start_date=dt.datetime(2024, 1, 1),
    # end_date=dt.datetime(2024, 1, 3),
    schedule_interval="@daily",
) as dag:
    fetch_ratings = DockerOperator(
        task_id="fetch_ratings",
        image="ssupecial-airflow/movielens-fetch",
        command=[
            "fetch-ratings",
            "--start_date",
            "{{ds}}",
            "--end_date",
            "{{next_ds}}",
            "--output_path",
            "/data/ratings/{{ds}}.json",
            "--user",
            os.environ["MOVIELENS_USER"],
            "--password",
            os.environ["MOVIELENS_PASSWORD"],
            "--host",
            os.environ["MOVIELENS_HOST"],
        ],
        network_mode="airflow",
        container_name="fetch-ratings-test",
        auto_remove=True,
        # Note: this host path is on the HOST, not in the Airflow docker container.
        mounts=[Mount(source="/Users/admin/Desktop/data", target="/data", type="bind")],
    )
    rank_movies = DockerOperator(
        task_id="rank_movies",
        image="ssupecial-airflow/movielens-ranking",
        command=[
            "rank_movies.py",
            "--input-path",
            "/data/ratings/{{ ds }}.json",
            "--output-path",
            "/data/rankings/{{ ds}}.csv",
        ],
        network_mode="bridge",
        mounts=[Mount(source="/Users/admin/Desktop/data", target="/data", type="bind")],
    )

    fetch_ratings >> rank_movies
