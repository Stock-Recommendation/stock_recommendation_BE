from django.urls import path
from . import views
urlpatterns = [
    path('<int:pk>/',views.cart_detail_view )
]
