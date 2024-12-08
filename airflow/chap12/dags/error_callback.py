from airflow import DAG
from airflow.operators.bash_operator import BashOperator


def send_error_email(context):
    print("Sending email to admin")


"""
DAG Failure Callback
"""
with DAG(
    dag_id="error_callback",
    schedule_interval=None,
    on_failure_callback=send_error_email,
) as dag:
    failing_task = BashOperator(
        task_id="failing_task",
        bash_command="exit 1",
    )

"""
Task Failure Callback
"""
with DAG(
    dag_id="task_error_callback",
    schedule_interval=None,
    default_args={"on_failure_callback": send_error_email},
) as dag:
    failing_task = BashOperator(
        task_id="failing_task",
        bash_command="exit 1",
    )
