# from airflow.operators.dummy import DummyOperator # Deprecated
from airflow.operators.empty import EmptyOperator
from airflow import DAG
import airflow.utils.dates

with DAG(
    dag_id="cycle_dag",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@once"
) as dag:
    t1 = EmptyOperator(task_id="t1")
    t2 = EmptyOperator(task_id="t2")
    t3 = EmptyOperator(task_id="t3")

    # This should be failed because of DAG cycle
    # t1 >> t2 >> t3 >> t1 
    
    t1 >> t2 >> t3
