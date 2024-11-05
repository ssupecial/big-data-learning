import os

from airflow.operators.bash import BashOperator
import airflow.utils.dates
from airflow import DAG


def generate_dag(dataset_name, raw_dir, processed_dir, preprocess_script, output_dir):
    """주어진 데이터셋에 대한 fetch, preprocess, export 태스크 체인을 생성합니다.

    Args:
        dataset_name      (str)        : 처리할 데이터셋의 이름
        raw_dir           (str)        : 원본 데이터를 저장할 디렉토리 경로
        processed_dir     (str)        : 전처리된 데이터를 저장할 디렉토리 경로
        preprocess_script (str)        : 데이터 전처리에 사용할 스크립트 파일명
        output_dir        (str)        : 최종 출력 데이터를 저장할 디렉토리 경로

    Returns:
        airflow.DAG: dag - 태스크 체인으로 구성된 DAG 객체
    """
    with DAG(
        dag_id=f"02_dag_factory_{dataset_name}",
        start_date=airflow.utils.dates.days_ago(5),
        schedule_interval="@daily",
    ) as dag:
        raw_path = os.path.join(raw_dir, dataset_name, "{ds_nodash}.json")
        processed_path = os.path.join(processed_dir, dataset_name, "{ds_nodash}.json")
        output_path = os.path.join(output_dir, dataset_name, "{ds_nodash}.json")

        fetch_task = BashOperator(
            task_id=f"fetch_{dataset_name}",
            bash_command=(
                f"echo 'curl http://example.com/{dataset_name}.json"
                f"> {raw_path}.json"
            ),
            dag=dag,
        )

        preprocess_task = BashOperator(
            task_id=f"preprocess_{dataset_name}",
            bash_command=f"echo '{preprocess_script} {raw_path} {processed_path}'",
            dag=dag,
        )

        export_task = BashOperator(
            task_id=f"export_{dataset_name}",
            bash_command=f"echo 'cp {processed_path} {output_path}'",
            dag=dag,
        )

        fetch_task >> preprocess_task >> export_task

    return dag


"""
# 최소한의 DAG 파일 사용
dag = generate_dag(
    dataset_name="sales",
    raw_dir="/data/raw",
    processed_dir="/data/processed",
    output_dir="/data/output",
    preprocess_script="preprocess_sales.py",
)
"""

"""하나의 DAG 파일을 사용하여 여러 DAG 생성"""
for dataset in ["sales", "customers"]:
    globals()[f"02_dag_factory_{dataset}"] = generate_dag(
        dataset_name=dataset,
        raw_dir="/data/raw",
        processed_dir="/data/processed",
        output_dir="/data/output",
        preprocess_script=f"preprocess_{dataset}.py",
    )
