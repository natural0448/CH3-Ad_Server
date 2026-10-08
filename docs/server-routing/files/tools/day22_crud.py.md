# tools/day22_crud.py

## 22일차·23일차2교시 교안기준 최종 구현

22일차2교시CRUD완성 code block29. 기존ads.env/root.env경로와MONGO_DB기본값만적응했다. 최상위에서practice_campaigns의_id=practice-campaign,priority=1,creative.headline=연습용지도안내/body=숲지도를살펴보세요 문서한건만insert→전체/projection조회→body한필드수정→priority3→해당문서delete→close한다. 실제campaigns/bids/ad_events는호출하지않는다. 이미같은연습ID가있으면DuplicateKeyError를임의삭제로해소하지않는다.
