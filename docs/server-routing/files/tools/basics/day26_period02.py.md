# tools/basics/day26_period02.py

교안2교시의 current_version/current_document 초급 코드 전체를 기존 tools/basics 한 파일에 이어 저장했다. 함수/클래스/CLI인수는 없다. 모듈 실행/import에서 즉시print한다.

versions 초기값은[1,4,2], chosen=0이며 큰 정수일 때만 갱신한다. 중간 출력은1,4,4다. document는_id=sample:member/version3/deletedFalse, candidate는sample-current/v1 schema를 추가한 새사전, current는빈사전, old는get결과None이다. 처음/큰version 후보를 저장하여3과sample-current/v1을 출력한다. 직접 호출 dict.get와print다. 실제project/Player/Mongo/file은 조작하지 않는다.
