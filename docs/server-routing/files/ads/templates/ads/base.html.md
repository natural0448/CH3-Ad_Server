# ads/templates/ads/base.html

기존 static 광고주 CSS/JS와 topbar·로그아웃 폼을 유지한다. `title`/`content`는 자식 template block이고 기본 title은 "마을 광고 스튜디오"다. `user`와 `request`는 Django template context다.

로그인한 사용자의 메뉴는 `ads:campaigns`, `ads:bids`, `ads:web-events`, `ads:web-reports`다. 보고서 메뉴는 `request.resolver_match.url_name == 'web-reports'`이면 `aria-current="page"`를 표시한다. 현재 URL을 다른 계층 상태로 저장하거나 서버를 호출하지 않는다.

기존 `user.username` 계정 표시와 POST `logout`/`{% csrf_token %}` 폼을 보존한다. 계정 표시와 비밀값 표시를 혼동하지 않는다. 비밀번호·매체 키는 표시하지 않으며 실제 CSRF 토큰은 문서/검증 파일에 기록하지 않는다. 직접 호출 관계는 Django URL 역참조·static template tag와 자식 block 렌더다. 기존 footer 문구도 유지한다.

이번 변경은 보고서 메뉴 한 항목과 해당 메뉴의 현재 페이지 표시다. 그 외 기존 base 내용을 재구성하지 않았다.
