from airflow.operators.dummy import DummyOperator
from airflow import DAG
import airflow.utils.dates

with DAG(
    dag_id="cycle_dag",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@once"
) as dag:
    t1 = DummyOperator(task_id="t1")
    t2 = DummyOperator(task_id="t2")
    t3 = DummyOperator(task_id="t3")

    t1 >> t2 >> t3 >> t1