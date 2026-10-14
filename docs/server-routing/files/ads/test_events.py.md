# ads/test_events.py

격리 ADS_TEST_MONGO_URI의 UUID DB에서 최초/중복/동시12회 사건, 당시 금액, 선행 노출, 수신자·내장 필드 순서·과거 스냅샷 검증을 확인한다. 두 매체 헤더·HTTP 오류 코드·POST·장애 계약과 광고주 owner 범위·최신 정렬·읽기만으로 사건 미생성·최초 시각 표시를 검사한다. create_ad_indexes는 반복 가능한 고유 색인과 정확한 출력으로 검증한다. 테스트 소유 DB만 정리한다. 실제 계정/키/수업 DB를 사용하지 않는다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `class EventAuthTests(SimpleTestCase)`

기반 클래스: SimpleTestCase. 메서드와 상태는 아래 계약을 따른다.

## `EventAuthTests.test_both_media_headers_must_match_the_authenticated_body(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `list`, `patch`, `record.assert_not_called`, `response.json`, `self.assertEqual`, `self.client.post`, `self.subTest`.

## `EventAuthTests.test_public_snapshot_error_keeps_only_the_allowed_error_code(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `ValueError`, `json.dumps`, `patch`, `response.json`, `self.assertEqual`, `self.client.post`.

## `EventAuthTests.test_media_key_json_subject_and_post_are_required(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `Client`, `client.get`, `client.post`, `json.dumps`, `patch`, `record.assert_not_called`, `self.assertEqual`, `self.subTest`.

## `EventAuthTests.test_store_outage_is_503_and_no_private_exception_is_exposed(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `PyMongoError`, `json.dumps`, `patch`, `response.json`, `self.assertEqual`, `self.client.post`.

## `class EventIntegrationTests(TestCase)`

기반 클래스: TestCase. 메서드와 상태는 아래 계약을 따른다.

## `EventIntegrationTests.test_subject_field_order_does_not_change_recipient_identity(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `record_ad_event`, `self.assertTrue`, `self.database.decisions.update_one`.

## `EventIntegrationTests.test_old_incomplete_snapshot_is_rejected_without_backfilling(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `record_ad_event`, `self.assertEqual`, `self.assertRaisesRegex`, `self.database.ad_events.count_documents`, `self.database.decisions.find_one`, `self.database.decisions.update_one`.

## `EventIntegrationTests.test_index_command_is_repeatable_and_prints_the_lesson_name(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `StringIO`, `call_command`, `output.getvalue`, `output.getvalue().strip`, `range`, `self.assertEqual`, `self.assertTrue`, `self.database.ad_events.index_information`.

## `EventIntegrationTests.test_advertiser_page_lists_only_owner_decisions_latest_first_without_events(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `PyMongoError`, `choose_ad`, `get_user_model`, `get_user_model().objects.create_user`, `patch`, `record_ad_event`, `self.assertContains`, `self.assertEqual`, `self.assertNotContains`, `self.client.force_login`, `self.client.get`, `self.client.post`, `self.database.ad_events.count_documents`, `self.database.decisions.insert_one`.

## `EventIntegrationTests.setUpClass(cls)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| cls | 없음 | 테스트 클래스; UUID fixture 연결/DB 상태 소유. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `MongoClient`, `super`, `super().setUpClass`, `uuid.uuid4`.

Decorator: `classmethod`.

## `EventIntegrationTests.tearDownClass(cls)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| cls | 없음 | 테스트 클래스; UUID fixture 연결/DB 상태 소유. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `cls.connection.close`, `cls.connection.drop_database`, `super`, `super().tearDownClass`.

Decorator: `classmethod`.

## `EventIntegrationTests.setUp(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `call_command`, `choose_ad`, `fixture.start`, `patch`, `self.addCleanup`, `self.database.bids.insert_one`, `self.database.campaigns.insert_one`, `self.database[name].delete_many`.

## `EventIntegrationTests.test_first_duplicate_click_and_snapshot_amount(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `record_ad_event`, `self.assertEqual`, `self.assertFalse`, `self.assertTrue`, `self.database.ad_events.count_documents`, `self.database.ad_events.find_one`, `self.database.bids.update_one`.

## `EventIntegrationTests.test_click_before_impression_wrong_subject_and_empty_decision(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `choose_ad`, `record_ad_event`, `self.assertEqual`, `self.assertRaises`, `self.database.ad_events.count_documents`, `self.subTest`.

## `EventIntegrationTests.test_concurrent_duplicates_have_one_first_write(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `ThreadPoolExecutor`, `list`, `pool.map`, `range`, `record_ad_event`, `self.assertEqual`, `self.assertTrue`, `self.database.ad_events.count_documents`, `self.database.ad_events.index_information`, `sum`.

## `EventIntegrationTests.test_invalid_types_and_missing_candidate_are_input_errors(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `record_ad_event`, `self.assertRaises`, `self.database.decisions.update_one`, `self.subTest`.

## `EventIntegrationTests.test_real_media_event_endpoint_duplicate_and_nonhashable_type(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `Client`, `client.post`, `duplicate.json`, `first.json`, `json.dumps`, `override_settings`, `self.assertEqual`, `self.assertFalse`, `self.assertTrue`.

Decorator: `override_settings(MEDIA_KEYS={'village-game': 'test-event-key'})`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.


## class ContextApiTests(SimpleTestCase)

25일차 context 회귀 검사를 기존 테스트 파일에 추가했다. 실제 키/업무 DB를 쓰지 않고 override_settings와 get_context patch를 사용한다. 모든 test 메서드의 self는 기본값 없는 테스트 인스턴스, 정상 반환 None, 실패 AssertionError다. 테스트 키·공개 ID·context는 이 클래스의 synthetic fixture이며 기존 EventAuthTests/EventIntegrationTests 본문은 보존했다.

### ContextApiTests.post_context(self, body=None, **headers)

body는 기본 None일 때 공개 subject 사전을 생성하고, 지정 시 JSON 본문으로 보낸다. headers는 기본 인증 fixture의 헤더를 덮어쓸 kwargs다. 반환은 Django Client response다. 의사코드: 본문·인증 fixture 구성 → headers.update → client.post. 직접 호출은 json.dumps, self.client.post이며 /api/media/context/의 실제 resolver를 사용한다.

### ContextApiTests.test_subject_only_payload_and_all_media_routes(self)

의사코드: context/decision/events resolve callable 확인 → 공개 lookup mock → subject-only POST → 200·공개 context·subject·no-store와 lookup 대상 검사. 직접 호출은 resolve, patch, post_context, response.json, lookup.assert_called_once_with와 assert 메서드다.

### ContextApiTests.test_invalid_headers_and_cross_media_subject_never_lookup(self)

의사코드: 누락·틀린 키/헤더 각 401 → 다른 매체 subject 400 → 모든 거절에서 lookup 미호출. 직접 호출은 patch, post_context, subTest, assert_not_called/assertEqual이다.

### ContextApiTests.test_legacy_top_level_media_id_remains_checked(self)

의사코드: 같은 top-level 매체 기존 본문은 200 → 불일치 매체는 401·조회 없음. 직접 호출은 patch, post_context와 assert다. 조회 전 인증 경계를 검증한다.

### ContextApiTests.test_method_rejection_is_json_and_has_allow(self)

의사코드: GET → 405·Allow POST·method_not_allowed JSON 검사. 직접 호출은 self.client.get, response.json와 assert다.

### ContextApiTests.test_empty_context_and_store_outage_are_distinct(self)

의사코드: 빈 조회 200/{} → PyMongoError fixture 503/ads_unavailable, 내부 실패 문자열 비노출. 직접 호출은 patch, post_context, response.json와 assert다. 원본 Mongo 문서를 생성·삭제하지 않는다.


## class ContextHandoffTests(SimpleTestCase)

8교시 파일 인계 검사를 기존 테스트 파일에 추가했다. 실제 MongoDB는 mock, 원문·checkpoint·인계 폴더는 각 테스트가 소유한 TemporaryDirectory에서 생성/정리한다. 기존 테스트 클래스 본문은 보존했다. 모든 메서드의 self는 기본값 없는 테스트 인스턴스, 정상 반환 None, 검증 실패 AssertionError다.

### ContextHandoffTests.setUp(self)

의사코드: TemporaryDirectory와 cleanup 등록 → 공개 Player 1/2 snapshot 두 개 normalize_snapshot → write_ndjson 입력 SHA → _save_context_checkpoint 완료 위치2 → 삭제 fixture 변경의 정렬 SHA → make_context_document 공개 저장 문서 세 개 → get_db 응답 Mock 구성. 직접 호출은 tempfile, Path, normalize_snapshot, write_ndjson, _save_context_checkpoint, json.dumps/hashlib.sha256, make_context_document, Mock다. self.source/checkpoint/target/state/checksum/fixture/documents/database는 해당 인스턴스 소유다. 날짜·ID·coins·version은 테스트용 공개 fixture다.

### ContextHandoffTests.test_four_files_preserve_input_and_replay_has_no_writes(self)

의사코드: export 실행 → 네 파일·두 SHA·경로·fixture 집계 검사 → 원문/완료 bytes 보존 → 인계 사본 project_context_file은 처리0·done true·apply 미호출. 직접 호출은 export_context_handoff, project_context_file, Path 읽기, JSON/SHA, patch와 assert다.

### ContextHandoffTests.test_existing_destination_is_not_overwritten(self)

의사코드: 기존 target/sentinel 생성 → export ValueError → DB 미조회·sentinel/list 불변. 직접 호출은 Path.mkdir/write_text/read_text/iterdir, export, patch와 assert다.

### ContextHandoffTests.test_wrong_or_incomplete_checkpoint_never_creates_output(self)

의사코드: 위치1·다른 SHA·bool 위치 각각 기록 → export ValueError → DB 미조회·target 없음. 직접 호출은 JSON/Path 쓰기, export, patch, subTest와 assert다. 원문 fixture는 보존한다.

### ContextHandoffTests.test_only_selected_media_player_snapshot_input_is_exported(self)

의사코드: 유효한 다른 매체 입력 또는 teaching-fixture 입력과 같은 SHA의 완료 기록 → export 지정 매체 오류 → DB 미조회·target 없음. 직접 호출은 normalize_snapshot, write_ndjson, _save_context_checkpoint, export, patch와 assert다.

### ContextHandoffTests.test_public_document_key_type_and_digest_are_checked(self)

의사코드: 잘못된 _id·int deleted·다른 change_id·추가 private 필드의 저장 문서 mock → _read_handoff_context 거절. 직접 호출은 helper, patch, subTest/assertRaises다. 실제 저장소를 변경하지 않는다.

### ContextHandoffTests.test_changed_copy_is_rejected_without_publishing_partial_bundle(self)

의사코드: copyfile 대신 바뀐 bytes를 쓴 nested changed_copy callback → export ValueError → target 없음·입력/기록 불변·임시 인계 정리 확인. callback changed_copy(source, destination)는 원래 복사 함수의 인수를 받고 destination에 테스트 bytes를 쓰며 None을 반환한다. 직접 호출은 Path.write_bytes/read_bytes/glob, export, patch와 assert다.

### ContextHandoffTests.test_command_exports_and_reports_existing_target_as_command_error(self)

의사코드: call_command export와 Mock DB → stdout JSON의 완료 위치2 확인 → 같은 target 재요청 CommandError. 직접 호출은 StringIO, call_command, patch, JSON과 assert다.


## class PlayerLakeTests(SimpleTestCase)

26일차1·2교시 회귀검사를 기존 테스트 파일에 추가했다. self는 각 메서드의 기본값 없는 테스트인스턴스, 정상 반환None, 실패AssertionError다. 기존 테스트 클래스 본문은 보존했다. fixture는 demo의 고정 teaching-fixture이고 파일검사만 테스트 소유TemporaryDirectory를 사용한다. 실제 Mongo는 mock이며 이번 관련 검사33개가 통과했다.

### PlayerLakeTests.test_history_repeated_reversed_and_equal_time_rows_are_deterministic(self)

의사코드: fixture 목록deepcopy → history → 반복/역순 같은결과·시각/동시각ID정렬·입력보존·JSON키순서 독립 확인. 직접 호출 fixture_change/copy.deepcopy/build_history/stable_json/sorted와assert다.

### PlayerLakeTests.test_schema_and_content_hash_are_validated_before_results(self)

의사코드: 잘못된schema 또는 내용과 다른SHA → build_history 거절. 직접 호출 fixture_change/build_history/subTest/assertRaises다.

### PlayerLakeTests.test_current_chooses_highest_version_and_preserves_input(self)

의사코드: version1/4/2 → 한10필드 current의version4/coins40 확인 → 반복/역순 같은결과·입력보존. 직접 호출 fixture_change/build_current/copy.deepcopy와assert다.

### PlayerLakeTests.test_latest_tombstone_cannot_be_revived_by_old_upsert(self)

의사코드: delete4/upsert2 → 최신삭제4/context{} 확인. 직접 호출 fixture_change/build_current와assert다.

### PlayerLakeTests.test_same_version_conflict_and_next_call_are_isolated(self)

의사코드: valid SHA의version4/coins40과99 충돌거절 → 다음 정상호출coins40 → 빈history/current 정상[]. 직접 호출 fixture_change/build_current/build_history/assertRaisesRegex/assertEqual다.

### PlayerLakeTests.test_media_are_distinct_and_provenance_ties_are_stable(self)

의사코드: 같은subject의 다른media를별도키로 계산 → 같은삭제상태/version의다른event_time SHA 후보를 역순으로 주어도 같은최소change_id 선택. 직접 호출 fixture_change/copy.deepcopy/stable_json/hashlib.sha256/build_current/min와assert다.

### PlayerLakeTests.test_preview_command_checks_manifest_checkpoint_and_preserves_files(self)

의사코드: 임시공개입력/완료기록/manifest → current 반복/역순조회 → N=1/supplied2/H=K=1/writtenFalse/원문bytes보존/DB미호출 → 미완료와manifest SHA불일치 CommandError. 직접 호출 TemporaryDirectory/Path/normalize_snapshot/write_ndjson/_save_context_checkpoint/call_command/StringIO/patch/JSON와assert다. 함수의 반환계약과 실제 명령 경계를 검사한다.

### PlayerLakeTests.test_demo_observes_duplicates_delete_conflict_and_empty_without_db(self)

의사코드: 정상4fixture사례의행수/미작성/DB미호출 → 잘못된schema·change ID·같은version충돌은 성공stdout 없이CommandError. 직접 호출 call_command/StringIO/patch/JSON/subTest/assertRaises와assert다.
