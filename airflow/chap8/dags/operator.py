from airflow import DAG 
from airflow.models import BaseOperator
from airflow.operators.python import PythonOperator
from airflow.utils.decorators import apply_defaults
from custom.operators import MovielensFetchRatingsOperator

import pandas as pd
import datetime as dt
import os
import json

with DAG(
    dag_id="fetch_by_operator",
    start_date=dt.datetime(2019,1,1),
    end_date=dt.datetime(2019,1,10),
    schedule_interval="@daily",
    max_active_runs=1,
) as dag:
    fetch_ratings = MovielensFetchRatingsOperator(
        task_id="fetch_ratings",
        conn_id="movielens",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
        output_path="/opt/airflow/data/python/ratings/{{ds}}.json"
    )

    def _rank_movies(templates_dict, min_ratings=2, **_):
        input_path = templates_dict["input_path"]
        output_path = templates_dict["output_path"]

        ratings = pd.read_json(input_path)
        ranking = rank_movies_by_rating(ratings, min_ratings=min_ratings)

        # Make sure output directory exists.
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        ranking.to_csv(output_path, index=True)

    def rank_movies_by_rating(ratings, min_ratings=2):
        ranking = (
            ratings.groupby("movieId")
                .agg(
                    avg_ratings = pd.NamedAgg(column="rating", aggfunc="mean"),
                    num_ratings = pd.NamedAgg(column="userId", aggfunc="nunique")
                )
                .loc[lambda df: df["num_ratings"] > min_ratings]
                .sort_values(["avg_ratings", "num_ratings"], ascending=False)
            )
        return ranking

    rank_movies = PythonOperator(
        task_id="rank_movies",
        python_callable=_rank_movies,
        templates_dict={
            "input_path": "/opt/airflow/data/python/ratings/{{ds}}.json",
            "output_path": "/opt/airflow/data/python/rankings/{{ds}}.csv",
        },
    )


    fetch_ratings >> rank_movies