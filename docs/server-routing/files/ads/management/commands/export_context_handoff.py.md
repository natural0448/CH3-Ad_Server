# ads/management/commands/export_context_handoff.py

25일차 8교시의 제공 관리명령을 기존 ads/management/commands 폴더에 저장했다. 실행 명령 이름은 export_context_handoff다. 새로운 서버/앱 폴더를 만들거나 기존 snapshot 인계 명령을 교체하지 않는다.

## class Command(BaseCommand)

help는 `검증한 입력·완료 기록·현재 공개 복사본을 새 인계 폴더로 묶습니다.`다. 옵션 작성자는 이 클래스이며 기본 media_id의 출처는 settings.ADS_MEDIA_ID다.

## Command.add_arguments(self, parser)

self는 Command, parser는 Django ArgumentParser이며 기본값 없다. 반환 None. 필수 문자열 --source·--checkpoint·--output-dir를 등록하고 --media-id는 settings.ADS_MEDIA_ID 기본값으로 등록한다. 입력은 최신 정규화 NDJSON·같은 입력의 완료 JSON·기존에 없는 인계 폴더 경로다. 직접 호출은 parser.add_argument다.

## Command.handle(self, *args, **options)

self는 Command, args는 미사용 Django 위치 인수, options는 위 네 옵션 사전이다. 반환 None, 성공 반환 사전은 ensure_ascii=False JSON으로 stdout에 기록한다. 의사코드: export_context_handoff(source, checkpoint, output_dir, media_id) → OSError/ValueError/TypeError/KeyError/PyMongoError를 CommandError로 연결 → JSON stdout. 직접 호출은 ads.context_projection.export_context_handoff, json.dumps, self.stdout.write다. 파일 쓰기·조회와 보호 검사는 하위 함수가 담당하며 이 클래스가 Mongo 문서를 쓰지 않는다.
