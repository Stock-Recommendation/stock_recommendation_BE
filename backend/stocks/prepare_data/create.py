import finnhub  # https://finnhub.io/docs/api/introduction
import pandas as pd
import calendar
import datetime
from datetime import datetime, timedelta, timezone
from stocks.models import Stock
import cronjobs

todayUTC = datetime.now(timezone.utc)
lastYearUTC = todayUTC - timedelta(365)
utc_time_to = calendar.timegm(todayUTC.utctimetuple())
utc_time_from = calendar.timegm(lastYearUTC.utctimetuple())
finnhub_client = finnhub.Client(api_key="cbdmpuaad3i64n13s900")
# ML model with cronjobs scheduled
# consider putting @cronjobs.register here


def process(stock) -> pd.DataFrame:
    tweet_ids = []
    historical_price = finnhub_client.stock_candles(
        stock, 'M', utc_time_from, utc_time_to)['c']
    time_stamp = finnhub_client.stock_candles(
        stock, 'M', utc_time_from, utc_time_to)['t']
    predicted_price_1d = predicted_price_1w = predicted_price_1m = predicted_price_3m = max(
        historical_price)+1
    return [predicted_price_1d, predicted_price_1w, predicted_price_1m, predicted_price_3m]

# main function to process everything with cronjobs scheduled


@cronjobs.register
def create():
    stocks = finnhub_client.indices_const(symbol="^OEX")['constituents'][:30]

    for stock in stocks:
        comp_info = finnhub_client.company_profile2(symbol=stock)
        ticker = stock
        stock_name = comp_info["name"]
        market_cap = comp_info["marketCapitalization"]
        current_price = finnhub_client.quote(stock)["c"]
        predicted_price_1d, predicted_price_1w, predicted_price_1m, predicted_price_3m = process(stock)[0], process(stock)[
            1], process(stock)[2], process(stock)[3]

        # get list of tweet ids for this stock here

        st = Stock(ticker=ticker, stock_name=stock_name,
                   market_cap=market_cap, current_price=current_price,
                   predicted_price_1d=predicted_price_1d, predicted_price_1w=predicted_price_1w, predicted_price_1m=predicted_price_1m, predicted_price_3m=predicted_price_3m)

        # if stock already exists, update
        if (len(Stock.objects.filter(ticker=stock)) != 0):
            stid = Stock.objects.get(ticker=stock).id
            oldSt = Stock.objects.get(id=stid)
            oldSt.ticker = ticker
            oldSt.stock_name = stock_name
            oldSt.market_cap = market_cap
            oldSt.current_price = current_price
            oldSt.predicted_price_1d = predicted_price_1d
            oldSt.predicted_price_1w = predicted_price_1w
            oldSt.predicted_price_1m = predicted_price_1m
            oldSt.predicted_price_3m = predicted_price_3m
        else:
            st.save()
