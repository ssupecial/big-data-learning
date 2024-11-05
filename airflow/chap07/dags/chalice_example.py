import json 
from io import BytesIO

import boto3
import numpy as np
from PIL import Image
from chalice import Chalice, Response
from sagemaker.amazon.common import numpy_to_record_serializer

app = Chalice(app_name="number_classifier")

@app.route("/", methods=["POST"], content_types=["image/jpeg"])
def predict():
    """
    이 엔드포인트에 jpeg 포맷의 이미지를 제공함.
    이 이미지는 학습 이미지와 사이즈가 동일해야함.
    """
    img = Image.open(BytesIO(app.current_request.raw_body)).convert("L")
    img_arr = np.array(img, dtype=np.float32)
    runtime = boto3.Session().client(
        service_name="sagemaker-runtime",
        region_name="eu-west-1"
    )
    response = runtime.invoke_endpoint(
        EndpointName="mnistClassifier",
        ContentType="application/x-recordio-protobuf",
        Body=numpy_to_record_serializer()(img_arr.flatten())
    )
    result = json.loads(response["Body"].read().decode("utf-8"))
    return Response(
        result, status_code=200, headers={"Content-Type": "application/json"}
    )


"""
요청 예시
curl --request POST \
    --url http://localhost:8080/ \
    --header 'content-type: image/jpeg' \
    --data-binary @'/path/to/image.jpeg'
"""