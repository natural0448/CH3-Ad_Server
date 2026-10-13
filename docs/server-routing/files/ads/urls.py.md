# ads/urls.py

`app_name = 'ads'`. urlpatterns는 기존 combined views의 광고주 웹 네 경로다. 모듈이 django.urls.path를 직접 호출하며 인증/메서드 검사는 각 view 책임이다.

| 경로 | 직접 callable | URL 이름 |
|---|---|---|
| advertiser/campaigns/ | views.campaign_view | ads:campaigns |
| advertiser/bids/ | views.bid_view | ads:bids |
| advertiser/events/ | views.advertiser_event_view | ads:web-events |
| advertiser/reports/ | views.report_view | ads:web-reports |

25일차 7교시에서 매체 decision/events/context는 상위 api/media/ include의 ads.media_urls로 일원화했다. 광고주 로그인·폼·보고서 경로와 combined views는 보존했다. 기존 공개 매체 주소는 같고 매체 reverse namespace는 media_ads다. 저장소 내 ads:decision/ads:events reverse 호출은 검색에서 없었다.
