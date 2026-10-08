# ads/templates/ads/bids.html

bid_view의 bids/message와 로그인 세션을 소비한다. CSRF POST campaign_id/bid_amount(1..10000)로 현재 입찰을 저장한다. 캠페인 저장 화면 링크와 현재 입찰 카드가 있으며 결제·노출 기록은 호출하지 않는다.
