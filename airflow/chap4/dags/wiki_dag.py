import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="wiki-dag",
    description="Fetches data from the Wikipedia API.",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
    catchup=False
) as dag:
    get_data = BashOperator(
        task_id="get_data",
        bash_command=(
            "curl -o /tmp/wikipageviews.gz "
            "https://dumps.wikimedia.org/other/pageviews/"
            "{{ execution_date.year }}/"
            "{{ execution_date.year }}-{{ '{:02}'.format(execution_date.month) }}/" # 패딩 문자열 빈 앞자리를 0으로 채워서 길이를 2로 맞춤
            "pageviews-{{ execution_date.year }}"
            "{{ '{:02}'.format(execution_date.month) }}{{ '{:02}'.format(execution_date.day) }}-"
            "{{ '{:02}'.format(execution_date.hour) }}0000.gz"
        )
    )

    get_data