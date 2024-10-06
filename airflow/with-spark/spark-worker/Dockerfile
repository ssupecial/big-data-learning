FROM apache/spark:v3.3.0

# Set the permissions for /opt/spark
USER root
RUN mkdir -p /opt/spark/work-dir && \
    chown -R 185:185 /opt/spark

# Switch back to the default user
USER 185

# Set the environment variables
ENV SPARK_MODE=worker \
    SPARK_MASTER_URL=spark://spark-master:7077 \
    SPARK_WORKER_MEMORY=1G \
    SPARK_WORKER_CORES=1 \
    SPARK_RPC_AUTHENTICATION_ENABLED=no \
    SPARK_RPC_ENCRYPTION_ENABLED=no \
    SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no \
    SPARK_SSL_ENABLED=no

# Command to start the worker
CMD ["/bin/bash", "-c", "/opt/spark/sbin/start-worker.sh spark://spark-master:7077 && tail -f /dev/null"]
