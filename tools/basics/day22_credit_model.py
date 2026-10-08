"""22일차 8교시의 별도 정산 모형; 실제 MongoDB 원장은 변경하지 않는다."""


def main():
    # 입력: 선충전액, 사건별 가격, 중복 전달된 전환 한 건.
    wallet = {"advertiser_id": "advertiser-a", "balance_credits": 100}
    prices = {"impression": 2, "click": 0, "conversion": 20}
    events = [
        {"event_id": "view-1", "event_type": "impression"},
        {"event_id": "click-1", "event_type": "click"},
        {"event_id": "sale-1", "event_type": "conversion"},
        {"event_id": "sale-1", "event_type": "conversion"},
    ]
    counts = {"impression": 0, "click": 0, "conversion": 0}
    seen = set()
    ledger = []

    # 처리: 고유 실적 집계와 성공한 차감을 각각 남긴다.
    for event in events:
        event_id = event["event_id"]
        if event_id in seen:
            continue
        seen.add(event_id)
        kind = event["event_type"]
        counts[kind] += 1
        amount = prices[kind]
        if amount == 0:
            continue
        if wallet["balance_credits"] < amount:
            print("차감 미승인", event_id)
            continue
        wallet["balance_credits"] -= amount
        ledger.append({"charge_key": "charge:" + event_id, "amount_credits": amount})

    print("통계", counts)
    print("차감", sum(row["amount_credits"] for row in ledger))
    print("잔액", wallet["balance_credits"])


if __name__ == "__main__":
    main()
