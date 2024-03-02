from django.urls import path
from .views import *

urlpatterns = [
    path('create/lease/', CreateHouseLease.as_view(), name='create_house_lease'),
    path('create/sale/', CreateHouseSale.as_view(), name='create_house_sale'),
    path('manage-lease/<int:lease_id>/', ManageHouseLease.as_view(), name='manage_lease'),
    path('leased-houses/', ListLeasedHouses.as_view(), name='leased_houses'),
    path('houses-for-sale/', ListHousesForSale.as_view(), name='houses_for_sale'),
    path('houses-for-rental/', ListHousesForRental.as_view(), name='houses_for_rental'),
]
