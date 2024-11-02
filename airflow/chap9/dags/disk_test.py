import json
import csv
from pathlib import Path
from airflow.models.baseoperator import BaseOperator


class JsonToCsvOperator(BaseOperator):
    """Json 파일을 CSV 파일로 저장하는 Operator"""

    def __init__(self, input_path, output_path, **kwargs):
        super().__init__(**kwargs)
        self._input_path = input_path
        self._output_path = output_path

    def execute(self, context):
        with open(self._input_path, "r") as json_file:
            data = json.load(json_file)

        # Json의 모든 행의 key를 순회하면서 유니크한 컬럼 추출
        columns = {key for row in data for key in row.keys()}

        with open(self._output_path, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)


def test_json_to_csv_operator(tmp_path: Path):
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.csv"

    # 입력 Json 파일 생성
    input_data = [
        {"name": "bob", "age": "41", "sex": "M"},
        {"name": "alice", "age": "24", "sex": "F"},
        {"name": "carol", "age": "60", "sex": "M"},
    ]
    with open(input_path, "w") as f:
        f.write(json.dumps(input_data))

    operator = JsonToCsvOperator(
        task_id="test",
        input_path=input_path,
        output_path=output_path,
    )

    operator.execute(context={})

    with open(output_path, "r") as f:
        reader = csv.DictReader(f)
        result = [dict(row) for row in reader]

    assert result == input_data
