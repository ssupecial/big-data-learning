import os
import datetime as dt

from kubernetes.client import models as k8s

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

volume_claim = k8s.V1PersistentVolumeClaimVolumeSource(
    claim_name="data-volume",
)
volume = k8s.V1Volume(
    name="data-volume",
    persistent_volume_claim=volume_claim,
)
volume_mount = k8s.V1VolumeMount(
    name="data-volume",
    mount_path="/data",
    sub_path=None,
    read_only=False,
)

with DAG(
    dag_id="02_kubernetes",
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 3),
    schedule_interval="@daily",
    catchup=True,
) as dag:
    fetch_ratings = KubernetesPodOperator(
        task_id="fetch_ratings",
        image="ssupecial-airflow/movielens-fetch",
        cmds=["fetch-ratings"],
        arguments=[
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
        namespace="airflow",
        name="fetch-ratings",
        cluster_context="minikube",
        in_cluster=False,
        volumes=[volume],
        volume_mounts=[volume_mount],
        image_pull_policy="Never",
        is_delete_operator_pod=True,
    )

    rank_movies = KubernetesPodOperator(
        task_id="rank_movies",
        image="ssupecial-airflow/movielens-rank",
        cmds=["rank-movies"],
        arguments=[
            "--input_path",
            "/data/ratings/{{ds}}.json",
            "--output_path",
            "/data/rankings/{{ds}}.csv",
        ],
        namespace="airflow",
        name="rank-movies",
        cluster_context="minikube",
        in_cluster=False,
        volumes=[volume],
        volume_mounts=[volume_mount],
        image_pull_policy="Never",
        is_delete_operator_pod=True,
    )

    fetch_ratings >> rank_movies
