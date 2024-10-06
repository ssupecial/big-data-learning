# word_count.py
from pyspark.sql import SparkSession

# Spark 세션을 생성
spark = SparkSession.builder.appName("WordCount").getOrCreate()

# 처리할 데이터 (여기서는 간단히 하드코딩된 리스트)
data = [
    "Apache Spark is amazing",
    "Apache Airflow is powerful",
    "Spark and Airflow together",
]

# 데이터를 RDD로 변환
rdd = spark.sparkContext.parallelize(data)

# 단어를 분리하고 각 단어의 빈도를 계산
word_counts = (
    rdd.flatMap(lambda line: line.split(" "))
    .map(lambda word: (word, 1))
    .reduceByKey(lambda a, b: a + b)
)

# 결과를 콘솔에 출력
word_counts.foreach(lambda pair: print(f"Word: {pair[0]}, Count: {pair[1]}"))

# Spark 세션 종료
spark.stop()
