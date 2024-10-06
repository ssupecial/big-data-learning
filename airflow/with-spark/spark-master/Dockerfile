FROM apache/spark:v3.3.0

# Jupyter Notebook 설치에 필요한 패키지 설치
USER root
RUN apt-get update && apt-get install -y python3-pip wget && \
    pip3 install jupyter pyspark ipykernel pymysql sqlalchemy cryptography pandas

# MySQL Connector/J 다운로드 및 설치 (JDBC 드라이버)
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.23.tar.gz && \
    tar -xzf mysql-connector-java-8.0.23.tar.gz && \
    cp mysql-connector-java-8.0.23/mysql-connector-java-8.0.23.jar /opt/spark/jars && \
    rm -rf mysql-connector-java-8.0.23 mysql-connector-java-8.0.23.tar.gz

# hadoop-aws 및 aws-java-sdk-bundle 다운로드 및 설치
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar -P /opt/spark/jars && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar -P /opt/spark/jars/


# 환경 변수 설정
ENV PYSPARK_PYTHON=python3
ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_WEBUI_PORT=8080

# Jupyter Notebook의 기본 포트 노출
EXPOSE 8888 8080 7077

# 기본 작업 디렉토리 설정
WORKDIR /opt/spark/work-dir

# 시작 스크립트 복사
COPY start.sh /opt/spark/start.sh
RUN chmod +x /opt/spark/start.sh

# 시작 스크립트를 사용하여 Jupyter Notebook과 Spark Master 실행
CMD ["/opt/spark/start.sh"]