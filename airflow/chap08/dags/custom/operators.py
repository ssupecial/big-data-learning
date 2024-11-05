from airflow import DAG 
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from custom.hooks import MovielensHook
import os
import json

class MovielensFetchRatingsOperator(BaseOperator):
    """
    Operator that fetches ratings from the Movielens API
    Movielens API로부터 rating(별점 정보)를 가져오는 오퍼레이터

    Params
    -----------
    conn_id: str
        ID of the connection to use to connect to the Movielens API.
        Connection is expected to inlcude authentication details(Login, Password)
        Movielens API에 연결할 컨넥션 아이디.
        Airflow Connections에 등록되어있어야하며, Login/Password 정보도 등록되어있어야함
    output_path: str
        Path to write the fetched ratings to.
    start_date: str
        (Templated) start date to start fetching ratings from (inclusive).
        Expected format is YYYY-MM-DD (Airflow ds format)
    end_date: str
        (Templated) end date to fetching ratings up to (exclusive)
        해당 날짜는 데이터에 포함 안됨
    """

    template_fields = ("_start_date", "_end_date", "_output_path")
    @apply_defaults
    def __init__(self, conn_id, output_path, start_date="{{ds}}", end_date="{{next_ds}}", **kwargs):
        super(MovielensFetchRatingsOperator, self).__init__(**kwargs)
        self._conn_id = conn_id
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date 

    def execute(self, context):
        # MovielensHook 인스턴스 생성
        hook = MovielensHook(self._conn_id)

        try:
            self.log.info(
                f"Fetching ratings for {self._start_date} to {self._end_date}"
            )
            ratings = list(
                hook.get_ratings(
                    start_date=self._start_date,
                    end_date=self._end_date
                )
            )
            self.log.info(f"Fetched {len(ratings)} ratings")

        finally:
            hook.close()

        self.log.info(f"Writing ratings to {self._output_path}")
        output_dir = os.path.dirname(self._output_path)
        os.makedirs(output_dir, exist_ok=True)

        with open(self._output_path, "w") as file_:
            json.dump(ratings, fp=file_)