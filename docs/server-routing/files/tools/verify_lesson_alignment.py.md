# tools/verify_lesson_alignment.py

원본22일차 및 수정23일차 v2.3의 HTML pre 코드와 현재 구현을 AST로 비교한다. 검사23개: 함수/실습 파일/색인 명령/실적 표. DEFAULT_DAY22와 DEFAULT_DAY23은 Desktop의 사용자 교안 파일, ROOT는 ad_server, WORKSPACE는 Chapter3다. 허용 적응은 기존4인수·스키마·이미지·환경·combined 모듈·타입 검사이며 결과 JSON에 명시한다. 이전 교안의 자동 접속기 기능은 preexisting_period3_client_mapping으로 구분한다. 서버/DB 호출은 하지 않는다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `class CodeBlocks(HTMLParser)`

기반 클래스: HTMLParser. 메서드와 상태는 아래 계약을 따른다.

## `CodeBlocks.__init__(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None.

의사코드: HTMLParser 초기화 → in_pre=False/current=[]/blocks=[].

직접 호출: `super`, `super().__init__`.

## `CodeBlocks.handle_starttag(self, tag, attrs)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |
| tag | 없음 | HTML tag 문자열. |
| attrs | 없음 | HTMLParser 속성 목록; 사용하지 않는다. |

반환·실패: None.

의사코드: tag가pre이면 current=[] 및 in_pre=True.

직접 호출: .

## `CodeBlocks.handle_endtag(self, tag)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |
| tag | 없음 | HTML tag 문자열. |

반환·실패: None.

의사코드: tag가pre이면 in_pre=False → current를 join해 blocks.append.

직접 호출: `''.join`, `self.blocks.append`.

## `CodeBlocks.handle_data(self, data)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |
| data | 없음 | 캠페인 입력 mapping 또는 HTMLParser 문자 데이터. |

반환·실패: None.

의사코드: in_pre일 때 current에 data append.

직접 호출: `self.current.append`.

## `read_blocks(path)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| path | 없음 | UTF8 교안 파일 Path. |

반환·실패: list[str].

의사코드: UTF8 파일 → CodeBlocks.feed → blocks 반환.

직접 호출: `CodeBlocks`, `parser.feed`, `path.read_text`.

## `function_ast(code, name)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| code | 없음 | 파싱할 Python 소스 str. |
| name | 없음 | 비교할 함수 이름 str. |

반환·실패: AST str; 문법 오류/함수 없음 예외.

의사코드: ast.parse → module의 지정 함수 검색 → 위치를 제외한 ast.dump.

직접 호출: `ast.dump`, `ast.parse`, `isinstance`, `next`.

## `main()`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| 없음 | — | 인자 없음 |

반환·실패: 성공False(프로세스0), 불일치True(프로세스1).

의사코드: 교안/출력 인자 → pre 읽기 → 비교23개와 적응 목록 → hash/JSON 저장 → 결과 출력.

직접 호출: `(ROOT / 'ads/templates/ads/events.html').read_text`, `(ROOT / 'tools/basics/day22_credit_model.py').read_text`, `(ROOT / relative).read_text`, `actual_table.splitlines`, `argparse.ArgumentParser`, `args.output.parent.mkdir`, `args.output.write_text`, `ast.Module`, `ast.dump`, `ast.parse`, `bool`, `compare`, `day22[59].rstrip`, `day22[67].replace`, `day22[block].replace`, `day23[15].replace`, `day23[16].replace`, `day23[21].replace`, `day23[22].split`, `day23[22].split('<div style="overflow-x:auto">')[1].split`, `day23[22].split('<div style="overflow-x:auto">')[1].split('</div>')[0].strip`, `expected.replace`, `failure.get`, `hashlib.sha256`, `hashlib.sha256(p.read_bytes()).hexdigest`, `isinstance`, `json.dumps`, `len`, `line.strip`, `next`, `p.read_bytes`, `parser.add_argument`, `parser.parse_args`, `print`, `read_blocks`, `reference_table.splitlines`, `results.append`, `service.replace`, `str`, `template.split`, `template.split('<div style="overflow-x:auto">')[1].split`, `template.split('<div style="overflow-x:auto">')[1].split('</div>')[0].strip`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
