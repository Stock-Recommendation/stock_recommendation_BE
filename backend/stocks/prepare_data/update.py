from stocks.models import Stock
import requests
def update_tweet_ids():
    allStocks = Stock.objects.all()
    endpoint = 'https://api.twitter.com/2/tweets/search/recent'
    bearerToken = "AAAAAAAAAAAAAAAAAAAAADNIgAEAAAAAlUftxzcQcUsX%2BLoMXypT4Ko%2FVzU%3DkK2Z0mfr2dGmQRlYWhxQt83N3PrrUru4hYuDghup0gNKzP3egS"
    header = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAADNIgAEAAAAAlUftxzcQcUsX%2BLoMXypT4Ko%2FVzU%3DkK2Z0mfr2dGmQRlYWhxQt83N3PrrUru4hYuDghup0gNKzP3egS"}
    # print(requests.get(endpoint, headers=header, data={'query': 'appl'}).json())
    
    for stock in allStocks:
        res = []
        tweetData = requests.get(endpoint, headers=header, data={'query': stock.ticker, 'tweet.fields': 'public_metrics'})
        # tweetId = map(tweetData.json(), lambda datapoint: datapoint)
        print(tweetData.json())
        stock.save()
    