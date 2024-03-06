from django.urls import path
from .views import *

urlpatterns = [
    path('create/land/buy', BuyLandCreateAPIView.as_view(), name='create_buy'),
    path('create/house/buy', BuyHouseCreateAPIView.as_view(), name='create_buy'),
]
