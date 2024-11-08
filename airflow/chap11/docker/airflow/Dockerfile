# Base image (Airflow)
FROM apache/airflow:2.10.2

# Set build arguments for UID and GID (use default 50000 if not provided)
ARG AIRFLOW_UID
ARG TARGETPLATFORM

# Set environment variables (if needed)
ENV AIRFLOW_HOME=/opt/airflow


USER root

# 방법 1: uname 명령어를 사용하여 실제 Linux 커널 확인
RUN if [ "$(uname)" = "Linux" ]; then \
        usermod -u $AIRFLOW_UID -g 0 airflow && \
        mkdir -p /opt/airflow/logs /opt/airflow/dags /opt/airflow/config /opt/airflow/plugins && \
        chown -R airflow: /opt/airflow/logs /opt/airflow/dags /opt/airflow/config /opt/airflow/plugins ; \
    else \
        echo "This setup must be run on Linux" && exit 1; \
    fi

# Set user to airflow (with modified UID and GID)
USER airflow
