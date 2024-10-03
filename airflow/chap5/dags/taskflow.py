from airflow.decorators import task 
from airflow.utils.dates import days_ago
from airflow import DAG 
import uuid

with DAG(
    dag_id="taskflow_test",
    start_date=days_ago(1),
    schedule_interval="@once"
) as dag:
    @task
    def train_model():
        model_id = str(uuid.uuid4())
        return model_id

    @task
    def deploy_model(model_id):
        print(f"Deploying model {model_id}")

    model_id = train_model()
    deploy_model(model_id)