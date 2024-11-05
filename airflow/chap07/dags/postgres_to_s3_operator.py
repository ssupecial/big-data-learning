import io
import os
import csv

from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

class PostgresToS3Operator(BaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_conn_id = kwargs.get('aws_conn_id')
        self.postgres_conn_id = kwargs.get('postgres_conn_id')
        self.bucket_name = kwargs.get('bucket_name')
        self.key = kwargs.get('key')
        self.query = kwargs.get('query')

        if not all([self.aws_conn_id, self.postgres_conn_id, self.bucket_name, self.key, self.query]):
            raise ValueError("Missing one or more required arguments: aws_conn_id, postgres_conn_id, bucket_name, key, query.")
    

    
    def execute(self, context):
        s3_hook = S3Hook(self.aws_conn_id)
        postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        results = postgres_hook.get_records(self.query)

        data_buffer = io.StringIO()
        csv_writer = csv.writer(data_buffer, lineterminator = os.linesep)
        csv_writer.writerows(results)

        data_buffer_binary = io.BytesIO(data_buffer.getvalue().encode())
        s3_hook.load_file_obj(
            file_obj=data_buffer_binary,
            bucket_name=self.bucket_name,
            key=self.key,
            replace=True
        )



