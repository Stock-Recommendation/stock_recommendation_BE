import finnhub  # https://finnhub.io/docs/api/introduction
import pandas as pd
import calendar
import datetime
from datetime import datetime, timedelta, timezone
from stocks.models import Stock

todayUTC = datetime.now(timezone.utc)
lastYearUTC = todayUTC - timedelta(365)

utc_time_to = calendar.timegm(todayUTC.utctimetuple())
utc_time_from = calendar.timegm(lastYearUTC.utctimetuple())

finnhub_client = finnhub.Client(api_key="cbdmpuaad3i64n13s900")
# print(res)
# print(pd.DataFrame(res))

stocks = finnhub_client.indices_const(symbol="^OEX")['constituents'][:30]

for stock in stocks:
    comp_info = finnhub_client.company_profile2(symbol=stock)
    ticker = stock
    stock_name = comp_info["name"]
    market_cap = comp_info["marketCapitalization"]
    # web_url = finnhub_client.company_profile2(symbol=stock)["weburl"]
    current_price = finnhub_client.quote(stock)["c"]
    # historical_price = finnhub_client.stock_candles(stock, 'D', utc_time_from, utc_time_to)
    st = Stock (ticker=ticker, stock_name=stock_name,
                         market_cap=market_cap, current_price=current_price)
    if (len(Stock.objects.filter(ticker=stock)) != 0):
        stid = Stock.objects.get(ticker=stock).id
        oldSt = Stock.objects.get(id=stid)
        oldSt.ticker = ticker
        oldSt.stock_name = stock_name
        oldSt.market_cap = market_cap
        oldSt.current_price = current_price
    else:
        st.save()
    