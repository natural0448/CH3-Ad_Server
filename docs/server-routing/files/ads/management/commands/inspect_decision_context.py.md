# ads/management/commands/inspect_decision_context.py

25일차 7교시 사용자 저장본은 제공 Command 클래스 AST와 같다. 실제 결정의 당시 context와 해당 대상의 현재 공개 context를 읽어 비교한다. 결정·Player·공개 복사본을 수정하지 않는다.

## class Command(BaseCommand)

help 초기값은 `선택 당시 context와 현재 공개 복사본을 읽기만 하여 비교합니다.`다. 옵션은 이 클래스가 소유하며 기본 매체는 settings.ADS_MEDIA_ID에서 읽는다.

## Command.add_arguments(self, parser)

self는 Command, parser는 Django ArgumentParser이고 기본값 없다. 반환은 None. 의사코드: 필수 상호 배타 그룹에 --decision-id/--subject → --latest store_true(default False) → --media-id(default settings.ADS_MEDIA_ID). 두 ID 옵션은 기본 None이며 둘 중 하나만 필수다. 직접 호출은 parser.add_mutually_exclusive_group와 add_argument다.

## Command.handle(self, *args, **options)

self는 Command, args는 미사용 위치 인수, options는 위 옵션 사전이다. 반환은 None이고 stdout에는 decision_id/subject/selected_at/context/current_context/same_context/differences JSON이 나온다. --decision-id는 비어 있지 않은 문자열이며 --latest와 같이 받지 않는다. --subject는 context_subject_key 계약을 만족하고 --latest가 필수다.

의사코드: 매체·subject 검사 → 매체 필터에 실제 _id 또는 subject_id 조건 구성 → decisions.find_one으로 selected_at 내림차순, 같은 시각 _id 내림차순 한 건 읽기 → 없음 거절 → 저장 context 복사 → get_context로 현재 복사본 → 필드 존재 여부와 값의 차이 계산 → 시각 ISO 변환 → stdout. 직접 호출은 context_subject_key, get_db().decisions.find_one, get_context, json.dumps, self.stdout.write다. find_one은 dict/None, get_context는 공개 dict를 반환한다. ValueError/TypeError/KeyError/PyMongoError는 CommandError다. latest는 화면의 결정 ID와 대조해야 하며 임의의 새 결정은 생성하지 않는다.
