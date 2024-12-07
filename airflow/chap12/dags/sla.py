"""
SLA: Service Level Agreement
"""

import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

with DAG(
    dag_id="task_sla",
    default_args={"email": "test@gmail.com"},
    schedule_interval=dt.timedelta(minutes=30),
    start_date=dt.datetime(2020, 1, 1, 12),
    end_date=dt.datetime(2020, 1, 1, 13),
) as dag:
    sleeptask = BashOperator(
        task_id="sleep_task",
        bash_command="sleep 60",
        sla=dt.timedelta(seconds=2),
    )
