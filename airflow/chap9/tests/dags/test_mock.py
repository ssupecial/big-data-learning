from pytest_mock import mocker
from airflow.models import Connection
from typing import Any
from collections import defaultdict, Counter
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow_movielens.hooks import MovielensHook

class MovielensPopularityOperator(BaseOperator):
    def __init__(self, conn_id, start_date, end_date, min_ratings=4, top_n=5, **kwargs):
        super().__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
        self._min_ratings = min_ratings
        self._top_n = top_n
    
    def execute(self, context: Context) -> Any:
        hook = MovielensHook(self._conn_id)
        # with MovielensHook(self._conn_id) as hook:
        ratings = hook.get_ratings(
            start_date = self._start_date,
            end_date = self._end_date
        )

        rating_sums = defaultdict(Counter)
        for rating in ratings:
            rating_sums[rating["movieId"]].update(
                count=1,
                rating=rating["rating"]
            )
        averages = {
            movie_id: (
                rating_counter["rating"] / rating_counter["count"],
                rating_counter["count"]
            )
            for movie_id, rating_counter in rating_sums.items()
            if rating_counter["count"] >= self._min_ratings
        }

        return sorted(
            averages.items(),
            key=lambda x:x[1],
            reverse=True
        )[:self._top_n]
    
def test_movielenspopularity(mocker):
    mock_get = mocker.patch.object(
        MovielensHook,
        "get_connection",
        return_value=Connection(
            conn_id="test",
            login="airflow",
            password="airflow",
            schema="http"
        )
    )

    task = MovielensPopularityOperator(
        task_id="test_id",
        conn_id="testconn",
        start_date="2015-01-01",
        end_date="2015-01-03",
        top_n=5
    )

    result = task.execute(context=None)
    assert len(result) == 5
    assert mock_get.call_count == 1
    mock_get.assert_called_with("testconn")