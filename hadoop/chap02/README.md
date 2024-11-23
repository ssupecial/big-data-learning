### 프로젝트 환경
💡 본 프로젝트는 Hadoop 환경을 Docker 컨테이너로 구성하였으며, 리눅스 원격 데스크탑과 로컬(Mac) IntelliJ를 이용하여 개발되었습니다.

- 로컬(Mac) IntelliJ: JAR 파일 구성
- 리눅스 원격 데스크탑: Hadoop 환경 구성 (Docker Container)

### 작업 흐름
[JAR 파일 구성 - 로컬 Mac IntelliJ] → 전송 → [하둡 환경 구성 - 리눅스 원격 데스크탑] → 실행


### 구성 및 실행
```
# 하둡 클러스터 실행
$ docker compose up -d

# JAR 파일 및 입력 데이터 전송
$ docker cp ./jar/${JAR 파일명}.jar namenode:/tmp
$ docker cp ./data/${SAMPLE 파일명}.txt namenode:/tmp

# HDFS 설정 및 Job 실행
$ docker exec -it namenode bash
root@namenode:/# hdfs dfs -mkdir -p /user/root/input
root@namenode:/# hdfs -put /tmp/${SAMPLE 파일명}.txt /user/root/input
root@namenode:/# hadoop jar /tmp/${JAR 파일명}.jar /user/root/input/temperature_sample.txt /user/root/output
```
결과 확인
```
root@namenode:/# hdfs dfs -ls /user/root/output
Found 2 items
-rw-r--r--   3 root supergroup          0 2024-11-23 15:39 /user/root/output/_SUCCESS
-rw-r--r--   3 root supergroup         17 2024-11-23 15:39 /user/root/output/part-r-00000

root@namenode:/# hdfs dfs -cat /user/root/output/part-r-00000
2024-11-23 15:54:02,467 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
1949    111
1950    22

```
- 사용한 샘플 파일
```
0067011990999991950051507004+68750+023550FM-12+038299999V0203301N00671220001CN9999999N9+00001+99999999999
0043011990999991950051512004+68750+023550FM-12+038299999V0203201N00671220001CN9999999N9+00221+99999999999
0043011990999991950051518004+68750+023550FM-12+038299999V0203201N00261220001CN9999999N9-00111+99999999999
0043012650999991949032412004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+01111+99999999999
0043012650999991949032418004+62300+010750FM-12+048599999V0202701N00461220001CN0500001N9+00781+99999999999
```
