# ads/urls.py

app_name=ads. urlpatterns는 기존 combined views와 루트 include 구조의 Django URLPattern 목록이다. advertiser/campaigns/→campaign_view(name=campaigns), advertiser/bids/→bid_view(name=bids), advertiser/events/→advertiser_event_view(name=web-events), api/media/decision/→decision_view(name=decision), api/media/events/→event_view(name=events). 새 실적 목록만 추가했고 기존 매체/광고주 경로는 보존했다. 직접 호출 path는 URLPattern을 반환한다. URL 메서드/인증은 각 view에서 처리한다.
