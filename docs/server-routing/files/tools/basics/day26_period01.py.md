# tools/basics/day26_period01.py

교안1교시의 history_keys/history_order 초급 코드 전체를 기존 tools/basics 한 파일에 이어 저장했다. 새 examples 디렉터리는 만들지 않았다. 함수/클래스/CLI인수는 없다. 모듈을 실행하거나 import하면 즉시 print한다.

codes 초기값은[a,a,b], unique는빈사전이며 반복문이 ID키로 값을 저장한다. left/right는 키순서만 다른 code=a/score2 사전, items는minute/code 세 행이다. sorted의 비교값은minute/code 튜플이고 원래items는 바뀌지 않는다. 직접 호출 json.dumps(sort_keys=True), sorted, list, len, print다. 실행 결과는 ['a', 'b'],2,True,['a', 'c', 'b']다. 파일/DB를 읽거나 쓰지 않는다.
