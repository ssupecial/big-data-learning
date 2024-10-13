from airflow.operators.bash import BashOperator

def test_example():
    task = BashOperator(
        task_id="test_bash",
        bash_command="echo 'hello!'",
        do_xcom_push=True
    )

    result = task.execute(context={})
    assert result == 'hello!'

if __name__ == "__main__":
    test_example()