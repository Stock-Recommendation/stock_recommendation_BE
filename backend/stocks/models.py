from django.db import models
# from .prepare_data import create
# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=4)
    # stock_id = models.IntegerField()
    stock_name = models.CharField(max_length=200)
    market_cap = models.IntegerField()
    current_price = models.FloatField(0.0)
    # time_stamp = models.DateTimeField()
    # stock_performance_graph = models.ImageField()
    # predicted_price_1d = models.FloatField()
    # predicted_price_1w = models.FloatField()
    # predicted_price_1m = models.FloatField()
    # predicted_price_3m = models.FloatField()
    # historical_accuracy = models.FloatField()

def create():
    Stock.objects.create(ticker="lasdla",stock_name="asda",market_cap=123123,current_price=123.1)
# update()
