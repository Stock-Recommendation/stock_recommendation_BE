from django.db import models
# from .prepare_data import create
# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=4, primary_key=True)
    stock_name = models.CharField(max_length=200)
    market_cap = models.IntegerField()
    current_price = models.FloatField(0.0)
    predicted_price_1d = models.FloatField()
    predicted_price_1w = models.FloatField()
    predicted_price_1m = models.FloatField()
    predicted_price_3m = models.FloatField()
    dummy = models.IntegerField(default=1)
    tweet_ids = models.CharField(max_length=1000, default='[]') #-> call on the front-ends
    
    # historical_price = models.IntegerField() -> call on the front-ends
    # time_stamp = models.DateTimeField() -> call on the front-ends
    # historical_accuracy = models.FloatField()
    # stock_id = models.IntegerField()

# update()
