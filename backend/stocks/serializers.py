from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            'ticker',
            # 'stock_id',
            'stock_name',
            'market_cap',
            'current_price',
            # 'stock_performance_graph',
            # 'predicted_price_1d',
            # 'predicted_price_1w',
            # 'predicted_price_1m',
            # 'predicted_price_3m',
            # 'historical_accuracy',
        ]
