# ads/templates/ads/base.html

기존 static 광고주 CSS/JS와 topbar·로그아웃 폼을 유지한다. title/content는 자식 template block, user는 Django 로그인 context다. 로그인한 사용자의 메뉴는 ads:campaigns/ads:bids/ads:web-events와 기존 POST logout/CSRF다. 새 선택·실적 메뉴만 추가했다. 계정·암호·매체 키는 표시하지 않는다.
