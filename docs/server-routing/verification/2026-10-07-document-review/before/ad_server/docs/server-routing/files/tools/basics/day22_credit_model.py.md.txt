# tools/basics/day22_credit_model.py

## 22일차·23일차2교시 교안기준 최종 구현

22일차8교시완성code block95를기존main진입점안에그대로두었다. wallet balance100,prices impression2/click0/conversion20,events고유노출/클릭/전환과중복전환,counts0,seen=set,ledger=[]는함수지역모형이다. 고유사건집계와차감승인분리,차감22/잔액78을출력한다. Mongo/실수업광고주원장에쓰지않는다.

### `main()`

| 파라미터 | 기본값 | 의미·허용범위 |
|---|---|---|

반환·실패: None;DB호출없음.

의사코드: 교안고정입력→고유사건집계→차감/잔액→출력.

직접호출: `set`, `print`, `seen.add`, `ledger.append`, `sum`. 호출결과는위반환·상태에사용하며하위내부구현은그짝문서가설명한다.
