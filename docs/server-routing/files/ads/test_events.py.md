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
