# ads/tests.py

광고주 로그인·CSRF·폼·소유자·입찰·소재·선택 API 회귀검사. ServingIntegrationTests는 ADS_TEST_MONGO_URI 아래 UUID 테스트 DB만 사용/정리한다. 새 bid 반환과 selected_at/owner 저장, BSON 밀리초 datetime decode, 정책 이름, 두 매체 헤더를 검증한다. 클래스의 계정/암호는 합성 fixture이며 실제 값은 문서화하지 않는다.

직접 호출의 기대 계약: get_db는 기존 Database, find_one은 dict/None, find·sort·limit는 Cursor, update_one은 UpdateResult, insert_one은 InsertOneResult, create_index는 색인 이름이다. Django render/JsonResponse는 HttpResponse, JSON parse는 dict 등 JSON 값, urlopen은 응답 stream, patch/assert는 테스트 fixture/검증을 제공한다. 하위 계층 내부는 해당 짝 문서에 있다.

## `class AuthenticationTests(TestCase)`

기반 클래스: TestCase. 메서드와 상태는 아래 계약을 따른다.

## `AuthenticationTests.setUpTestData(cls)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| cls | 없음 | 테스트 클래스; UUID fixture 연결/DB 상태 소유. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `get_user_model`, `get_user_model().objects.create_user`.

Decorator: `classmethod`.

## `AuthenticationTests.setUp(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `Client`.

## `AuthenticationTests.csrf_headers(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: 테스트 응답의 CSRF 값을 HTTP_X_CSRFTOKEN 키에 넣은 헤더 사전; 상태 검사 실패 AssertionError. 실제 토큰 값은 문서에 기록하지 않는다.

의사코드: 테스트 client로 GET /api/auth/csrf/ → 200 확인 → 응답 JSON의 csrfToken을 헤더 사전으로 반환.

직접 호출: `response.json`, `self.assertEqual`, `self.client.get`.

## `AuthenticationTests.test_csrf_cookie_and_get_only_endpoint(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `self.assertEqual`, `self.assertIn`, `self.client.post`, `self.csrf_headers`.

## `AuthenticationTests.test_login_requires_csrf(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `self.assertEqual`, `self.client.post`.

## `AuthenticationTests.test_invalid_login_bodies_are_rejected(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `response.json`, `self.assertEqual`, `self.client.post`, `self.csrf_headers`, `self.subTest`.

## `AuthenticationTests.test_incorrect_password_is_rejected(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `self.assertEqual`, `self.assertNotIn`, `self.client.post`, `self.csrf_headers`.

## `AuthenticationTests.test_login_and_logout_use_advertiser_session(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `response.json`, `self.assertEqual`, `self.assertIn`, `self.assertNotIn`, `self.client.post`, `self.csrf_headers`.

## `AuthenticationTests.test_admin_route_is_available(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `self.assertEqual`, `self.client.get`.

## `AuthenticationTests.test_browser_login_and_protected_pages(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `response.url.startswith`, `self.assertContains`, `self.assertEqual`, `self.assertRedirects`, `self.assertTrue`, `self.client.get`, `self.client.post`, `self.csrf_headers`.

## `AuthenticationTests.test_database_outage_is_a_rendered_503(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `PyMongoError`, `get_user_model`, `get_user_model().objects.get`, `patch`, `self.assertContains`, `self.assertEqual`, `self.client.force_login`, `self.client.get`.

## `AuthenticationTests.test_media_authentication_precedes_selection(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `choose.assert_not_called`, `json.dumps`, `override_settings`, `patch`, `self.assertEqual`, `self.client.post`.

## `class ServingIntegrationTests(TestCase)`

기반 클래스: TestCase. 메서드와 상태는 아래 계약을 따른다.

## `ServingIntegrationTests.setUpClass(cls)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| cls | 없음 | 테스트 클래스; UUID fixture 연결/DB 상태 소유. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `MongoClient`, `cls.connection.admin.command`, `super`, `super().setUpClass`, `uuid.uuid4`.

Decorator: `classmethod`.

## `ServingIntegrationTests.tearDownClass(cls)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| cls | 없음 | 테스트 클래스; UUID fixture 연결/DB 상태 소유. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `cls.connection.close`, `cls.connection.drop_database`, `super`, `super().tearDownClass`.

Decorator: `classmethod`.

## `ServingIntegrationTests.setUp(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; fixture 실패는 테스트 실패로 보고.

의사코드: 자기 테스트 클래스/메서드 fixture 준비·patch 또는 연결/UUID DB 정리. 실제 수업 DB를 사용하지 않는다..

직접 호출: `Client`, `get_user_model`, `get_user_model().objects.create_user`, `patch`, `patcher.start`, `self.addCleanup`, `self.client.force_login`, `self.database.list_collection_names`, `self.database[name].delete_many`.

## `ServingIntegrationTests.campaign(self, campaign_id, slot_id='village-board', active='on')`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |
| campaign_id | 없음 | 캠페인 ID 문자열; 쓰기 경로는 [a-z0-9_-]{1,40}. |
| slot_id | 'village-board' | village-board 또는 lobby-banner. |
| active | 'on' | 해당 소스에서 읽는 fixture/계층 입력; 소유한 테스트·호출 범위에서 사용한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_campaign`.

## `ServingIntegrationTests.test_owner_collision_keeps_original_document(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.get_campaign`, `repository.save_campaign`, `self.assertEqual`, `self.assertRaises`, `self.campaign`.

## `ServingIntegrationTests.test_invalid_campaign_fields_do_not_write(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_campaign`, `self.assertEqual`, `self.assertRaises`, `self.database.campaigns.count_documents`, `self.subTest`.

## `ServingIntegrationTests.test_bid_updates_one_document_and_rejects_bad_values(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.list_bids`, `repository.save_bid`, `self.assertEqual`, `self.assertRaises`, `self.campaign`, `self.database.bids.count_documents`, `self.database.bids.find_one`, `self.subTest`.

## `ServingIntegrationTests.test_bid_checks_owner_existence_and_active_status(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_bid`, `self.assertEqual`, `self.assertRaises`, `self.campaign`, `self.database.bids.count_documents`, `self.subTest`.

## `ServingIntegrationTests.test_bid_owner_collision_is_not_overwritten(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_bid`, `self.assertEqual`, `self.assertRaises`, `self.campaign`, `self.database.bids.find_one`, `self.database.bids.insert_one`.

## `ServingIntegrationTests.test_changed_bid_does_not_change_past_decision(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `first.items`, `first['selected_at'].replace`, `first['selected_at'].replace(tzinfo=None).isoformat`, `repository.save_bid`, `self.assertEqual`, `self.assertNotEqual`, `self.campaign`, `self.database.decisions.find_one`, `services.choose_ad`, `stored.items`, `stored['selected_at'].isoformat`.

## `ServingIntegrationTests.test_tie_slot_and_invalid_candidate_filtering(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_bid`, `self.assertEqual`, `self.campaign`, `self.database.bids.insert_one`, `services.choose_ad`.

## `ServingIntegrationTests.test_empty_selection_and_nested_context_snapshot(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `self.assertEqual`, `self.assertIsNone`, `self.assertRaises`, `self.database.decisions.count_documents`, `services.choose_ad`.

## `ServingIntegrationTests.test_web_forms_render_and_save_with_csrf(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.get_campaign`, `self.assertContains`, `self.assertEqual`, `self.client.get`, `self.client.post`.

## `ServingIntegrationTests.test_media_api_subject_validation_and_response(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `override_settings`, `repository.save_bid`, `response.json`, `self.assertEqual`, `self.campaign`, `self.client.post`, `self.database.decisions.count_documents`.

## `ServingIntegrationTests.test_media_api_empty_candidate_response(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `override_settings`, `response.json`, `self.assertEqual`, `self.client.post`, `self.database.decisions.count_documents`.

## `ServingIntegrationTests.test_shared_mongo_client_connects_and_closes(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `mongo.close_client`, `mongo.get_client`, `mongo.get_client.cache_info`, `mongo.get_db`, `mongo.get_db().command`, `override_settings`, `self.assertEqual`, `self.assertIs`.

## `ServingIntegrationTests.test_image_campaign_and_decision_keep_original_creative(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `json.dumps`, `override_settings`, `repository.save_bid`, `repository.save_campaign`, `response.json`, `self.assertEqual`, `self.client.post`, `self.database.decisions.find_one`, `services.choose_ad`.

## `ServingIntegrationTests.test_image_paths_reject_remote_traversal_and_missing_files(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_campaign`, `self.assertEqual`, `self.assertRaises`, `self.database.campaigns.count_documents`, `self.subTest`.

## `ServingIntegrationTests.test_campaign_edit_form_is_owner_scoped_and_contains_preview(self)`

| 파라미터 | 기본값 | 의미·허용 범위 |
|---|---|---|
| self | 없음 | 해당 인스턴스. 상태 쓰기는 해당 객체가 소유한다. |

반환·실패: None; 테스트 실패 AssertionError.

의사코드: 이름에 해당하는 fixture 준비 → 실제 함수/HTTP 호출 → 반환·상태·저장 불변식 assert → fixture 정리.

직접 호출: `repository.save_campaign`, `self.assertContains`, `self.assertNotContains`, `self.campaign`, `self.client.get`.

## 상태·값 출처

지역 변수는 해당 함수가 소유하며 request/입력·서버 설정·DB 조회 또는 위 의사코드의 생성 단계에서 얻는다. 저장 snapshot과 receipt의 쓰기는 서비스/사건 계층이 맡는다. 테스트 연결·patch·가짜 응답은 해당 테스트 클래스만 소유하고 정리한다. 비밀값·쿠키·CSRF 토큰은 문서/증거에 복사하지 않는다.
