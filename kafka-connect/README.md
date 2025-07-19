# Connector 목록
| 번호 | 이름    | 링크          | 라이센스 |
|------|---------|----------------|--------|
| 1    | Spooldir   | https://www.confluent.io/hub/confluentinc/kafka-connect-spooldir   | Apache License 2.0 | 
| 2    | JDBC       | https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc | Confluent Community License |

---

# 설치
```sh
$ docker compose up -d
```
### 설치 목록
- zookeeper
- kafka broker
- kafka connect
- kafka ui

---
### httpie 이용 및 커넥터 중지
```sh
$ brew install httpie
$ http PUT http://localhost:8083/connectors/csv_spooldir_source/pause
$ http PUT http://localhost:8083/connectors/csv_spooldir_source/resume
```

### kcat 
```sh
$ brew install kcat
# 토픽 확인
$ kcat -b localhost:9094 -L
# 메세지 구독
$ kcat -b localhost:9094 -C -t spooldir-csv
# 메세지 구독 (Key도 함께 출력)
$ kcat -b localhost:9094 -C -t spooldir-csv -K "###"
# 메세지 구독 (Json 포맷, 헤더 정보 함께 출력)
$ kcat -b localhost:9094 -C -t spooldir-csv -J | jq '.'
# 
$ kcat -b localhost:9094 -C -t spooldir-csv -Juq| jq '.'
# 메세지 구독 (포맷팅)
$ kcat -b localhost:9094 -Cuq -t spooldir-csv -f '\nKey: %k\nValue: %s\nPartition: %p\nOffset: %o\n\n'
# 메세지 구독 (특정 파티션만)
$ kcat -b localhost:9094 -Cuq -t connect-offsets -f '\nKey: %k\nValue: %s\nPartition: %p\nOffset: %o\n\n' -p 23

$ docker run 
$ kafka-topics.sh --bootstrap-server broker:9092 --create --topic kcat-test-topic
