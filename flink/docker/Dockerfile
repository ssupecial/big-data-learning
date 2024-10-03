# Flink 베이스 이미지 사용
FROM flink:1.20.0-scala_2.12-java17

# 작업 디렉토리 설정
WORKDIR /opt/flink-job

# 아키텍처에 따라 JAVA_HOME 설정
RUN arch=$(uname -m) && \
    if [ "$arch" = "x86_64" ]; then \
        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64; \
    elif [ "$arch" = "aarch64" ]; then \
        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64; \
    fi && \
    echo "export JAVA_HOME=$JAVA_HOME" >> /etc/profile && \
    echo "export PATH=$JAVA_HOME/bin:$PATH" >> /etc/profile

# 환경 변수 설정 (위에서 설정한 JAVA_HOME과 PATH를 불러오기)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
ENV PATH="$JAVA_HOME/bin:$PATH"

# 기본 커맨드 설정 (bash 사용)
CMD ["/bin/bash"]