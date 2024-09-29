from airflow import DAG
from airflow.operators.python import PythonOperator 
import airflow.utils.dates
import json

with DAG(
    dag_id="check-context-parameters",
    description="Print Context",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@once"
) as dag:
    def _print_context(**kwargs):
        print(kwargs)
    
    print_context = PythonOperator(
        task_id='print_context',
        python_callable=_print_context
    )

    print_context