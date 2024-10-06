FROM apache/airflow:2.5.1

USER root

RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get install -y ant && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN if [ "$(uname -m)" = "x86_64" ]; then \
        echo "Setting JAVA_HOME for amd64"; \
        export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"; \
    elif [ "$(uname -m)" = "aarch64" ]; then \
        echo "Setting JAVA_HOME for arm64"; \
        export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-arm64"; \
    else \
        echo "Unknown architecture"; \
        exit 1; \
    fi


ENV JAVA_HOME $JAVA_HOME
ENV PATH $JAVA_HOME/bin:$PATH


RUN curl -o /tmp/hadoop.tgz https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    && tar -xvzf /tmp/hadoop.tgz -C /opt/ \
    && mv /opt/hadoop-3.3.6 /opt/hadoop \
    && rm /tmp/hadoop.tgz


RUN curl -o /tmp/spark.tgz https://dlcdn.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz \
    && tar -xvzf /tmp/spark.tgz -C /opt/ \
    && mv /opt/spark-3.4.3-bin-hadoop3 /opt/spark \
    && rm /tmp/spark.tgz

# Spark와 관련된 환경 변수 설정
ENV SPARK_HOME /opt/spark/spark-3.4.3-bin-hadoop3
ENV PATH $SPARK_HOME/bin:$PATH

ENV HADOOP_HOME /opt/hadoop/hadoop-3.3.6
ENV PATH $HADOOP_HOME/bin:$PATH

ENV PYSPARK_PYTHON /usr/bin/python3

# 기본 작업 디렉토리
WORKDIR /opt/airflow

USER airflow
# PySpark 설치
RUN pip install pyspark

# Entrypoint 설정 (Airflow가 실행될 수 있도록 설정)
ENTRYPOINT ["/entrypoint"]
CMD ["bash"]
