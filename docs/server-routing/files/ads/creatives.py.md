# ads/creatives.py

## 22일차 이미지 광고 최종 반영

CREATIVES는 forest-tools/camp-tea 두 PNG의 path·label·theme(forest/tea) tuple이고 CREATIVE_PATHS는 이 path의 frozenset이다. 외부 URL·경로 조작·임의 파일을 허용하지 않는다. blank는 기존 문구 광고용이며 선택 시 로컬 실제 PNG 헤더까지 확인한다.

### `validate_creative(value)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| value | 없음 | 검증할 문자열/필드 값; 해당 함수의 허용 범위 참조. |

반환·실패: 허용 문자열 또는 ValueError.

의사코드: blank 또는 두 local PNG path 검사 → 파일 존재·PNG 헤더 확인 → 허용 path 반환.

직접 호출: `ValueError`, `isinstance`, `value.rsplit`, `file.is_file`, `Path`, `file.read_bytes`. 호출 결과는 이 함수의 반환·상태 갱신에 사용한다. 외부 계층의 내부 구현은 그 계층 문서에서 설명한다.
