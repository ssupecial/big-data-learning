import datetime as dt
import os
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG

with DAG(
    dag_id="01_docker",
    description="Fetches ratings from the Movielens API using Docker",
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 3),
    schedule_interval="@daily",
) as dag:
    fetch_ratings = DockerOperator(
        task_id="fetch_ratings",
        image="ssupecial-airflow/movielens-fetch",
        docker_url="unix://var/run/docker.sock",
        auto_remove="force",
        mount_tmp_dir=False,
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
        # 호스트 시스템내에 이미 데이터를 저장할 폴더를 생성해놓고, docker-compose.yml 환경변수로 넘겨주었음
        mounts=[
            Mount(source=os.environ["HOST_PATH"], target="/data", type="bind")
        ],  # 호스트 시스템 <-> movielens-fetch 도커 컨테이너
        network_mode="airflow",  # movielens-api 컨테이너와 같은 도커 네트워크여야함
    )

    rank_movies = DockerOperator(
        task_id="rank_movies",
        image="ssupecial-airflow/movielens-ranking",
        command=[
            "rank-movies",
            "--input_path",
            "/data/ratings/{{ds}}.json",
            "--output_path",
            "/data/rankings/{{ds}}.csv",
        ],
        mounts=[Mount(source=os.environ["HOST_PATH"], target="/data", type="bind")],
    )

    fetch_ratings >> rank_movies
