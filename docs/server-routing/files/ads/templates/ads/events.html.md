# ads/templates/ads/events.html

수정 교안 CODE22의 표와 빈 상태를 기존 ads/base.html에 연결한다. rows는 advertiser_event_view가 소유한 최대30개 자기 광고 결정의 decision_id/campaign_id/bid_amount/selected_at/snapshot_ready/impression/click이다. message는 저장소503 안내 또는 빈 값. 노출/클릭 없으면 미기록, snapshot_ready=False면 새 광고 요청 필요, rows가 비면 자기 결정 없음 안내. Django template가 값을 escape한다. 읽기 화면이며 HTTP 사건 POST/JS 저장 없음. bid 링크는 기존 ads:bids, reports 링크는 후속6교시 미구현이라 연결하지 않았다.
