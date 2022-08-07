from rest_framework import generics
from .models import Cart
from .serializers import CartSerializer

class CartDetailAPIView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
cart_detail_view = CartDetailAPIView.as_view()