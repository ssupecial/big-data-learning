# Connector 목록
| 번호 | 이름    | 링크          | 라이센스 |
|------|---------|----------------|--------|
| 1    | Spooldir   | https://www.confluent.io/hub/confluentinc/kafka-connect-spooldir   | Apache License 2.0 | 

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

# 실습
### Spooldir Source Connector (CSV)
```sh
# Spooldir 폴더 만들기
$ mkdir -p spooldir/{error,finished}

# 예제 데이터 다운로드
$ cd spooldir
$ wget https://raw.githubusercontent.com/chulminkw/KafkaConnect/main/sample_data/csv-spooldir-source.csv -O csv-spooldir-source-01.csv

# Spooldir Source 커넥터 등록
$ curl -X POST -H "Content-Type:application/json" http://localhost:8083/connectors --data @configs/csv_spooldir_source.json
# Spooldir Source 커넥터 확인
$ curl -X GET http://localhost:8083/connectors/csv_spooldir_source/status | jq 
```