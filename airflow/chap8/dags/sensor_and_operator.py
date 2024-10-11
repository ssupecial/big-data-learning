from airflow import DAG 
from custom.operators import MovielensFetchRatingsOperator
from custom.sensors import MovielensRatingsSensor
import airflow.utils.dates

import datetime as dt 
import pandas as pd
import os


with DAG(
    dag_id="sensor_and_hook",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
    max_active_runs=1
) as dag:
    wait_for_ratings = MovielensRatingsSensor(
        task_id="wait_for_ratings",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
        conn_id="movielens",
        poke_interval=10,
        timeout=60,
        soft_fail=True
    )

    fetch_ratings = MovielensFetchRatingsOperator(
        task_id="fetch_ratings",
        conn_id="movielens",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
        output_path="/opt/airflow/data/python/ratings/{{ds}}.json"
    )

    wait_for_ratings >> fetch_ratings