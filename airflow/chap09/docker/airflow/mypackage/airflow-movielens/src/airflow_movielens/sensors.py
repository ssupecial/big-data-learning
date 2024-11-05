from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from .hooks import MovielensHook

class MovielensRatingsSensor(BaseSensorOperator):
    """
    Sensor that watis for the Movielens API to have ratings for a time period
    해당 날짜에 평점 데이터가 있는지 확인

    start_date: str
    end_date: str
    """

    template_fields = ("_start_date", "_end_date")
    @apply_defaults
    def __init__(self, conn_id, start_date="{{ds}}", end_date="{{next_ds}}", **kwargs):
        super(MovielensRatingsSensor, self).__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date

    def poke(self, context):
        hook = MovielensHook(
            conn_id=self._conn_id
        )

        try:
            next( # 훅에서 레코드 하나를 가져오는 것을 시도
                hook.get_ratings(
                    start_date=self._start_date,
                    end_date=self._end_date,
                    batch_size=1 # 하나의 데이터만 가져옴
                )
            )
            self.log.info(f"Found ratings for {self._start_date} to {self._end_date}")
            return True
        except StopIteration:
            self.log.info(
                f"Didn't find any ratings for {self._start_date} to {self._end_date}"
            )
            return False
        finally:
            hook.close()