# config/mongo-node1.yml

dbPath=infra/mongo/data/node1, bindIp=localhost, port=27017, replSetName=ads-rs. 실행 위치는 ad_server다. 설정 파일만으로 프로세스가 시작되거나 replica가 초기화되지 않는다. 내부 데이터는 mongod가 쓴다. node1 단독 또는 세 노드 구성에 사용한다.
