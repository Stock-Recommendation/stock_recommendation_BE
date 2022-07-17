from statistics import mode
from django.http import JsonResponse, HttpResponse, HttpRequest
import json
from django.forms.models import model_to_dict
from products.models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response

# declare allowed methods


@api_view(['GET'])
def api_home(request: HttpRequest, *args, **kwargs):
    """DRF API View
    """
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'price'])
        print(data)
    return Response(data)
