# spark_submit_dag.py

from airflow import DAG
import airflow.utils.dates
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

# DAG 정의
with DAG(
    dag_id="spark_submit_example",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    # SparkSubmitOperator를 사용하여 PySpark 스크립트를 제출
    submit_spark_job = SparkSubmitOperator(
        task_id="submit_word_count_job",
        application="/shared/word_count.py",  # PySpark 스크립트 경로
        conn_id="spark_default",  # Spark 연결 ID (Airflow에 설정된 것)
        verbose=True,
    )

    submit_spark_job
