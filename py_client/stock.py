# import finnhub  # https://finnhub.io/docs/api/introduction
# import pandas as pd
# import calendar
# import datetime
# from datetime import datetime, timedelta, timezone
# # from stocks import Stock

# todayUTC = datetime.now(timezone.utc)
# lastYearUTC = todayUTC - timedelta(365)

# utc_time_to = calendar.timegm(todayUTC.utctimetuple())
# utc_time_from = calendar.timegm(lastYearUTC.utctimetuple())

# finnhub_client = finnhub.Client(api_key="cbdmpuaad3i64n13s900")
# # print(res)
# # print(pd.DataFrame(res))

# stocks = finnhub_client.indices_const(symbol="^OEX")['constituents'][:15]
# res = []
# for stock in stocks:
#     ticker = stock
#     name = finnhub_client.company_profile2(symbol=stock)["name"]
#     market_cap = finnhub_client.company_profile2(symbol=stock)["marketCapitalization"]
#     # web_url = finnhub_client.company_profile2(symbol=stock)["weburl"]
#     current_price = finnhub_client.quote(stock)["c"]
#     # print(stock)
#     res.append([ticker, name, market_cap, current_price])
# print(res)