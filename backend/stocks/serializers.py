from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            'ticker',
            'stock_name',
            'market_cap',
            'current_price',
            'predicted_price_1d',
            'predicted_price_1w',
            'predicted_price_1m',
            'predicted_price_3m',
            'dummy',
            'tweet_ids',
            # 'stock_performance_graph',
            # 'stock_id',
            # 'historical_accuracy',
        ]
