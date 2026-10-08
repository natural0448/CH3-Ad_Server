# ads/templates/ads/reports.html

2026-10-08 검증이 끝난 현재 템플릿이다. 작업 시작 시 교안 6교시의 독립 HTML을 사용하던 사용자 구현을 먼저 문서화한 뒤, 현재 광고 스튜디오 화면에 맞게 `ads/base.html`을 상속했다. 교안의 9개 출력 바인딩은 순서와 필터까지 그대로다. 변경 전 소스/문서는 `verification/day23-period06-template/before/`와 `user-code-documented/`에 보존했다.

`title` block은 "광고주 일별 보고서 · 마을 광고 스튜디오", `content` block은 제목·설명·표다. 제목 "내 광고 일별 보고서"를 유지하며 공통 상단/하단·CSS/JS는 base template이 제공한다. 직접 URL 역참조는 `ads:web-events`로 가는 "선택·실적 보기" 링크이고, 다른 광고주 메뉴는 base의 책임이다.

입력 context는 `report_view(request)`의 `rows` 사전 목록과 선택적 `message` 문자열이다. 소유자 필터링은 view/list_reports의 책임이다. 템플릿은 DB를 읽거나 사건/보고서를 생성하지 않는다.

표는 9개 열이다: 서울 날짜=`row.date`, 캠페인=`row.campaign_id`, 슬롯=`row.slot_id`, 노출=`row.impressions`, 클릭=`row.clicks`, CTR 0~1=`row.ctr|floatformat:3`, 모의 포인트 합=`row.bid_units_sum`, 원본 마지막 시각=`row.source_max_event_time`, 보고서 생성 시각=`row.generated_at`. 원본 ISO 시각 문자열을 그대로 표시하며 CTR을 백분율로 변환하지 않는다. 빈 rows는 colspan 9의 "게시된 내 보고서가 없습니다." 행을 표시한다. Django autoescape가 출력 필드에 적용된다.

고정 설명은 "노출일 기준 · 고정 입력 파일까지 관찰한 클릭입니다. 모의 포인트 합은 실제 청구액이 아닙니다."로 유지한다. `rows|length`는 표시된 보고서 행 수만 보여 주며 다른 지표를 계산하지 않는다. `message`가 있을 때 `notice error`와 `role="alert"`로 출력한다.

표의 직접 스타일 계약은 `report-card`, `report-table-scroll`, `report-table`, `report-number`, `report-date`, `report-id`, `report-time`, `report-empty`다. 표 영역은 `role="region"`, `aria-label="일별 보고서 표"`, `tabindex="0"`이고 각 열은 `scope="col"`이다. 좁은 화면에서 표 영역만 가로 스크롤하며 안내 문구를 제공한다. 정렬과 조회 범위는 reporting.list_reports가 정한 순서를 사용한다.

검증: RequestFactory의 가짜 rows로 정상/빈 목록/503/자동 escape/CTR/ISO 시각 유지와 로그인 이동/GET 제한을 확인했다. 현재 로그인된 실제 HTTP 페이지에서는 3개 보고서 행과 9개 열, 기본 화면 및 390px 화면을 관찰했다. 에이전트는 DB 게시와 서버 실행/종료를 수행하지 않았다.
