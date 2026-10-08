# ads/static/ads/advertiser.css

광고주 공통 UI를 cream/green, tea palette의 카드와 pixelated PNG로 그린다. workspace/login은 2열, campaign-grid는 3열이며 기존 800/480px media query에서 줄인다. 기존 파일 바이트는 보존하고 끝에 6교시 보고서 스타일만 추가했다. CSS 파일이 아래 표시 값을 소유하며 서버 계약이나 집계 데이터를 수정하지 않는다.

- `.topbar nav`: 추가 메뉴가 작은 화면에서 줄바꿈되도록 `flex-wrap:wrap`. `a[aria-current="page"]`는 굵기 800과 초록색 하단선으로 현재 보고서 페이지를 표시한다.
- `.report-heading`, `.report-note`, `.report-card`: 기존 제목·도움말·카드 색을 유지하며 간격과 `min-width:0`을 지정한다.
- `.report-table-scroll`: `max-width:100%`, `overflow-x:auto`, 테두리/12px 모서리. 표 때문에 페이지 전체가 가로로 늘어나지 않게 한다.
- `.report-table`: `width:100%`, `min-width:1000px`, 13px 글씨와 접힌 테두리. 헤더는 12px, 셀 여백은 14px/12px, 행 구분과 hover 배경을 제공한다.
- `.report-number`/`.report-date`: 숫자는 우측 정렬과 tabular-nums, 날짜/숫자 줄바꿈 제한. `.report-id`는 110~170px, `.report-time`은 150~185px 폭 기준과 긴 텍스트 줄바꿈을 제공한다. 원본 ISO 시각 문자열은 CSS가 변환하지 않는다.
- `.report-empty`: 44px/20px 여백과 중앙 정렬. `.report-scroll-hint`: 표 아래 안내 간격.
- 추가 480px media query: 메뉴 행/열 간격, 보고서 링크·설명 카드, 표 셀 여백만 조정한다.

기본 1280px viewport에서 페이지 가로 넘침이 없었고 표 영역 client/scroll 폭이 1040px로 같았다. 390px viewport에서는 페이지 client/scroll 폭이 모두 375px이며 표 영역만 295px/1000px로 가로 스크롤됨을 실제 브라우저에서 확인했다.
