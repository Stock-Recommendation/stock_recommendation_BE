from django.shortcuts import render
from .serializers import StockSerializer
from .models import Stock
from rest_framework.decorators import api_view
# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, mixins

#only allow get for client
@api_view(['GET'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == 'GET':
        if pk is not None:
            obj = get_object_or_404(Stock, pk=pk)
            data = StockSerializer(obj, many=False).data
            return Response(data)
        # no primary key, return all
        qs = Stock.objects.all()
        data = StockSerializer(qs, many=True).data
        return Response(data)
    return Response(data={"message":"unallowed method"}, status=403)
