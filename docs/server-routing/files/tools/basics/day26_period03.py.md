# tools/basics/day26_period03.py

26일차3교시 초급 예제 전체를 기존 tools/basics 배치로 적용했다. 새로운 examples 폴더는 만들지 않았다. 클래스·함수·파라미터·반환 정의는 없고 python tools/basics/day26_period03.py로 직접 실행한다.

의사코드: payload=b"same" → hashlib.sha256(payload).hexdigest() → digest 길이 출력 → 같은 bytes 지문 일치 출력. 직접 호출 hashlib.sha256/hexdigest, len, print다. payload는 모듈 작성자의 고정 bytes, digest는 실행 시 계산한64자리 SHA 문자열이다. 출력은64/True 두 줄이며 파일·MongoDB를 읽거나 쓰지 않는다. 마지막 b"same"을 b"different"로 바꾸는 학습 변경은False를 출력한다.
