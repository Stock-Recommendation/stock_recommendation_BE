from statistics import mode
from django.http import JsonResponse, HttpResponse, HttpRequest
import json
from django.forms.models import model_to_dict
from products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer
from carts.models import Cart
from carts.serializers import CartSerializer
# declare allowed methods


@api_view(['GET'])
def api_home(request: HttpRequest, *args, **kwargs):
    """DRF API View
    """
    instance = Product.objects.all().order_by("?").first()
    # instance = Cart.objects.all().order_by("?").last()
    data = {}
    if instance:
        # data = model_to_dict(model_data, fields=['id', 'price'])
        # data = CartSerializer(instance).data
        data=ProductSerializer(instance).data
        print(data)
    return Response(data)
