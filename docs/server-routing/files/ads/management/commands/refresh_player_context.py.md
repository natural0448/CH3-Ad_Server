# ads/management/commands/refresh_player_context.py

25일차 6교시 사용자 저장본은 제공 Command 클래스 AST와 같다. Django 관리명령에서 새 수신 snapshot·계약을 공개 context 갱신 함수에 전달한다.

## class Command(BaseCommand)

help 초기값은 `새 snapshot과 수신 계약을 대조한 뒤 공개 context를 갱신합니다.`다. CLI 옵션의 소유자는 add_arguments, 기본 매체의 출처는 settings.ADS_MEDIA_ID다. 비밀값은 출력하지 않는다.

## Command.add_arguments(self, parser)

self는 Command 인스턴스, parser는 Django ArgumentParser이며 기본값 없다. 반환은 None이다. 의사코드: 필수 --source·--contract 문자열 등록 → --media-id 문자열을 settings.ADS_MEDIA_ID 기본값으로 등록. 직접 호출은 parser.add_argument다. 경로의 실제 검증은 refresh_snapshot이 담당한다.

## Command.handle(self, *args, **options)

self는 Command, args는 Django가 전달한 위치 인수로 본문에서 쓰지 않으며 options는 파싱된 source/contract/media_id 사전이다. 반환은 None, 성공 요약은 stdout JSON이다. 의사코드: refresh_snapshot(source, contract, media_id) → OSError/ValueError/TypeError/KeyError/PyMongoError를 CommandError로 변환 → UTF-8 표시용 정렬 JSON stdout. 직접 호출은 ads.context_projection.refresh_snapshot, json.dumps, self.stdout.write다. 본 계층은 직접 파일·checkpoint·DB를 쓰지 않는다. 갱신 함수가 공개 복사본의 쓰기를 담당한다.
