# Base image (Airflow)
FROM apache/airflow:2.10.2

# Set build arguments for UID and GID (use default 50000 if not provided)
ARG AIRFLOW_UID
ARG TARGETPLATFORM

# Set environment variables (if needed)
ENV AIRFLOW_HOME=/opt/airflow


USER root

# Linux 환경일 경우, Airflow 관련 폴더 모두 권한 airflow로 수정
RUN if [ "$(uname)" = "Linux" ]; then \
        usermod -u $AIRFLOW_UID -g 0 airflow && \
        mkdir -p /opt/airflow/logs /opt/airflow/dags /opt/airflow/config /opt/airflow/plugins && \
        chown -R airflow: /opt/airflow/logs /opt/airflow/dags /opt/airflow/config /opt/airflow/plugins ; \
    else \
        echo "This setup must be run on Linux" && exit 1; \
    fi

# Set user to airflow (with modified UID and GID)
USER airflow
