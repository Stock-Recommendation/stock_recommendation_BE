from django.db import models
from prepare_data import create
# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=4)
    stock_id = models.IntegerField()
    # market_cap = models.IntegerField()
    # current_price = models.FloatField()
    # stock_performance_graph = models.ImageField()
    # predicted_price_1d = models.FloatField()
    # predicted_price_1w = models.FloatField()
    # predicted_price_1m = models.FloatField()
    # predicted_price_3m = models.FloatField()
    # historical_accuracy = models.FloatField()

# create()
update()