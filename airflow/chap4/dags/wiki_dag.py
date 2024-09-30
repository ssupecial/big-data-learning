import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from  urllib import request
from datetime import timedelta

with DAG(
    dag_id="wiki-dag",
    description="Fetches data from the Wikipedia API.",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@hourly",
    template_searchpath="/tmp",
    max_active_runs=1,
    catchup=False
) as dag:
    # Python Version 

    def _get_data_python(execution_date):
        previous_one_hour = execution_date - timedelta(hours=1)
        year, month, day, hour, *_ = previous_one_hour.timetuple()
        url = (
            "https://dumps.wikimedia.org/other/pageviews/"
            f"{ year }/{ year }-{month:0>2}/"
            f"pageviews-{ year }{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
        )
        output_path = "/tmp/wikipageviews.gz"
        request.urlretrieve(url, output_path)

    get_data = PythonOperator(
        task_id="get_data",
        python_callable=_get_data_python,
        op_kwargs = {
            'year': "{{ execution_date.year }}",
            'month': "{{ execution_date.month }}",
            'day': "{{execution_date.day}}",
            'hour': "{{execution_date.hour}}"
        }
    )

    '''
    # Bash 버전
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
    '''

    extract_gz = BashOperator(
        task_id='extract_gz',
        bash_command="gunzip --force /tmp/wikipageviews.gz"
    )

    def _fetch_pageviews(pagenames, execution_date, **context):
        result = dict.fromkeys(pagenames, 0)
        with open(f"/tmp/wikipageviews", "r") as f:
            for line in f:
                domain_code, page_title, view_counts, _ = line.split(" ")
                if domain_code == "en" and page_title in pagenames:
                    result[page_title] = view_counts

        # PostgrespOperator에 공급할 INSERT 구문 작성
        with open("/tmp/postgres_insert_query.sql", "w") as f:
            for pagename, pageviewcounts in result.items():
                f.write(
                    "INSERT INTO pageview_counts (pagename, pageviewcount, datetime) VALUES ("
                    f"'{pagename}', {pageviewcounts}, '{execution_date}'"
                    ");\n"
                )

    fetch_pageviews = PythonOperator(
        task_id='fetch_pageviews',
        python_callable=_fetch_pageviews,
        op_kwargs={
            'pagenames': {
                "Google",
                "Amazon",
                "Apple",
                "Microsoft",
                "Facebook"
            }
        }
    )

    write_to_postgres = PostgresOperator(
        task_id="write_to_postgres",
        postgres_conn_id="my_postgres",
        sql="postgres_insert_query.sql"
    )


    get_data >> extract_gz >> fetch_pageviews >> write_to_postgres