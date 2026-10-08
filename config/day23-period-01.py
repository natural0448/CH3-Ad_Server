bid = {"bid_units": 30}
decision = {"bid_units": bid["bid_units"]}
bid["bid_units"] = 40
print(bid["bid_units"], decision["bid_units"])
