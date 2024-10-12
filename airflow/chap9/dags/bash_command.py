import datetime as dt
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="bash_command",
    start_date=dt.datetime(2024, 10, 11),
    schedule_interval="@once"
):
    BashOperator(
        task_id="this_should_fail"
    )
