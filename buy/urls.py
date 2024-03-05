from django.urls import path
from .views import *

urlpatterns = [
    path('create/', BuyLandCreateAPIView.as_view(), name='create_buy'),
]
