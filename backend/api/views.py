from statistics import mode
from django.http import JsonResponse, HttpResponse, HttpRequest
import json
from django.forms.models import model_to_dict
from products.models import Product
def api_home(request: HttpRequest, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    # print(model_data)
    data= {}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'price'])
        json_data_str = json.dumps(data)
        print(data)
    # return HttpResponse(data), return type html/text
    # return HttpResponse(json_data_str, headers={'content-type': "application/json"}) 
    return JsonResponse(data)

