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
# Spooldir Source 커넥터 삭제
$ curl -X DELETE http://localhost:8083/connectors/csv_spooldir_source
```

- Message 확인
```sh
$ docker run --rm -it --network kafka-net bitnami/kafka:4.0 bash
I have no name!@03813397b616:/$ kafka-console-consumer.sh --bootstrap-server broker:9092 --topic spooldir-csv --from-beginning --property print.key=true
```