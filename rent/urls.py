from django.urls import path
from .views import *

urlpatterns = [
    path('create/house', RentHouseCreateAPIView.as_view(), name='create_rent'),
]
