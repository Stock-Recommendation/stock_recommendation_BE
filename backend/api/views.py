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

from django.http import JsonResponse
@api_view(['POST'])
def api_home(request: HttpRequest, *args, **kwargs):
    """DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid": "bad request"}, status=400)
