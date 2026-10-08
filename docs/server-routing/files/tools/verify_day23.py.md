# tools/verify_day23.py

기존 광고 표시·클릭 계층의 보조 통합 검사다. 최신 3교시의 공식 check_day23_period3 검증기가 아니다. 실제 HTTP/PNG/Pygame fixture로 연결한다. ROOT/WORKSPACE와 Web/child/wait_http는 verify_day22_images의 기존 fixture helper다. REPORT는 docs/server-routing/verification/day23-period03. 자기 UUID runtime, Mongo27109 ads-image-validation/image_validation, HTTP18000/18001과SQLite만 사용한다. 두 슬롯을 표시하고 마을 노출/클릭2건·당시 금액·createdFalse·확인 클릭 미재전송·광고주 events 페이지를 확인한다. Pygame은 SDL dummy이고 클릭은 모의 입력이다. actual_student_game_observation=not_run이며 실수업 DB와 실제 계정/키는 사용하지 않는다.

직접 호출 기대 계약: UI/상태 helper는 각 짝 문서의 반환 계약을 따른다. worker.submit은접수bool, HTTP/JSON helper는공개dict 또는공개오류, read_ad_event는id/type/created dict, emit은queue전달, create_task는Task, Pygame draw/decode는Surface/표시receipt, fixture Web은bytes이다. 하위 계층 내부를 복제하지 않는다.

## `render_flow(owned)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| owned | 없음 | 이검사가만든 UUID fixture runtime Path. |

반환·실패: async None; 실패AssertionError.

의사코드: fixture로그인/두슬롯선택 → 사건없음 및 advertiser행 → flip/impression → 모의마을click → 중복/웹/PNG증거 → 세션정리.

직접 호출: `(owned / 'render-result.json').write_text`, `AdGateway`, `AuthSession`, `Controller`, `InputRouter`, `InputRouter().route`, `Network`, `ScreenRenderer`, `Web`, `advertiser.get`, `advertiser.get('/advertiser/events/').decode`, `advertiser.post`, `all`, `any`, `auth.close`, `auth.login`, `auth.refresh_csrf`, `auth.request_json`, `build_layout`, `controller.ads.slots.values`, `controller.confirm_ad_display`, `controller.game.apply_identity`, `controller.game.apply_state`, `controller.game.apply_status`, `controller.handle_intent`, `controller.handle_network_event`, `controller.request_ad`, `controller.screen_model`, `duplicates.append`, `gateway.close`, `gateway.set_identity`, `json.dumps`, `load_config`, `pump`, `pygame.display.get_surface`, `pygame.display.init`, `pygame.display.set_mode`, `pygame.event.Event`, `pygame.font.init`, `pygame.image.save`, `pygame.quit`, `renderer.render`, `set`, `str`, `sys.path.insert`.

## `main()`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| 없음 | — | 인자없음 |

반환·실패: 성공0 또는예외.

의사코드: 인자/fixture포트 → 자기Mongo/HTTP process → 캠페인·입찰·render → 사건/당시값 검증 → 증거JSON → finally 종료.

직접 호출: `(REPORT / 'integration.json').write_text`, `(owned / 'render-result.json').read_text`, `MongoClient`, `REPORT.mkdir`, `RuntimeError`, `Web`, `advertiser.get`, `advertiser.post`, `all`, `argparse.ArgumentParser`, `asyncio.run`, `child`, `db.ad_events.count_documents`, `db.ad_events.create_index`, `db.ad_events.find`, `db.ad_events.find_one`, `dict`, `direct.admin.command`, `direct.admin.command('hello').get`, `direct.close`, `json.dumps`, `json.loads`, `len`, `list`, `log.close`, `mongo.poll`, `owned.mkdir`, `parser.add_argument`, `parser.error`, `parser.parse_args`, `print`, `process.poll`, `process.terminate`, `process.wait`, `range`, `render_flow`, `reversed`, `sock.bind`, `socket.socket`, `start`, `str`, `subprocess.run`, `time.sleep`, `uuid.uuid4`, `wait_http`.

## 상태·값 출처

지역 변수는 입력·기존 설정·검증한 공개응답·monotonic시간 또는 자기fixture에서 얻으며 해당함수/클래스가 쓴다. 전역/타이머/큐/fixture의 주요 초기값과 쓰기 소유자는 위 파일설명에 기록한다. 실제env값·계정암호·cookie·CSRF토큰은기록하지않는다.
