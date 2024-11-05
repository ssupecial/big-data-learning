from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
from airflow import DAG
import airflow.utils.dates

with DAG(
    dag_id="aws_s3",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@once"
) as dag:
    s3_copy_task = S3CopyObjectOperator(
        task_id="s3_copy_test",
        source_bucket_name="sw-coaching",
        source_bucket_key="candle/2024-08-21 07:57:01.parquet",
        dest_bucket_name="eunsu-code-sam-2",
        dest_bucket_key="test.parquet",
        aws_conn_id="aws_default",
    )
    s3_copy_task