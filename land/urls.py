from django.urls import path
from .views import *


urlpatterns = [
    path('create/', LandSellAPIView.as_view(), name='create_land'),
    path('', LandList.as_view(), name='lands'),
    path('user/', UserLandList.as_view(), name='user_land_list'),
    path('<int:pk>/', LandList.as_view(), name='land_retrieve'),
    path('<int:pk>/update/', LandUpdateAPIView.as_view(), name='land_update'),
    path('<int:pk>/delete/', LandDestroyAPIView.as_view(), name='land_delete'),
]