import os

from airflow.operators.bash import BashOperator
import airflow.utils.dates
from airflow import DAG


def generate_tasks(
    dataset_name, raw_dir, processed_dir, preprocess_script, output_dir, dag
):
    """주어진 데이터셋에 대한 fetch, preprocess, export 태스크 체인을 생성합니다.

    Args:
        dataset_name      (str)        : 처리할 데이터셋의 이름
        raw_dir           (str)        : 원본 데이터를 저장할 디렉토리 경로
        processed_dir     (str)        : 전처리된 데이터를 저장할 디렉토리 경로
        preprocess_script (str)        : 데이터 전처리에 사용할 스크립트 파일명
        output_dir        (str)        : 최종 출력 데이터를 저장할 디렉토리 경로
        dag               (airflow.DAG): 태스크를 추가할 Airflow DAG 객체

    Returns:
        tuple: (fetch_task, export_task) - 태스크 체인의 시작과 끝 태스크를 반환
              다른 태스크들과의 의존성 설정에 사용될 수 있음
    """
    raw_path = os.path.join(raw_dir, dataset_name, "{ds_nodash}.json")
    processed_path = os.path.join(processed_dir, dataset_name, "{ds_nodash}.json")
    output_path = os.path.join(output_dir, dataset_name, "{ds_nodash}.json")

    fetch_task = BashOperator(
        task_id=f"fetch_{dataset_name}",
        bash_command=(
            f"echo 'curl http://example.com/{dataset_name}.json" f"> {raw_path}.json"
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
    return (
        fetch_task,
        export_task,
    )  # 더 큰 그래프의 다른 태스크에 연결할 수 있도록 체인의 첫번째 태스크와 마지막 태스크를 반환(필요 시)


with DAG(
    dag_id="01_task_factory",
    start_date=airflow.utils.dates.days_ago(5),
    schedule_interval="@daily",
) as dag:
    for dataset in ["sales", "customers"]:
        generate_tasks(
            dataset_name=dataset,
            raw_dir="/data/raw",
            processed_dir="/data/processed",
            output_dir="/data/output",
            preprocess_script=f"preprocess_{dataset}.py",
            dag=dag,
        )
