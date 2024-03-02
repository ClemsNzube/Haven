from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import House
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *

class CreateHouseLease(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HouseLeaseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateHouseSale(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HouseSaleSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ManageHouseLease(APIView):
    def get_object(self, lease_id):
        try:
            return House.objects.get(pk=lease_id)
        except House.DoesNotExist:
            return Response({"error": "HouseLease with id {} does not exist".format(lease_id)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, lease_id, format=None):
        lease = self.get_object(lease_id)
        serializer = HouseLeaseSerializer(lease)
        return Response(serializer.data)

    def put(self, request, lease_id, format=None):
        lease = self.get_object(lease_id)
        serializer = HouseLeaseSerializer(lease, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, lease_id, format=None):
        lease = self.get_object(lease_id)
        serializer = HouseLeaseSerializer(lease, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, lease_id, format=None):
        lease = self.get_object(lease_id)
        lease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListLeasedHouses(APIView):
    def get(self, request, format=None):
        leased_houses = House.objects.filter(is_for_sale=False)
        serializer = HouseSerializer(leased_houses, many=True)
        return Response(serializer.data)

class ListHousesForSale(APIView):
    def get(self, request, format=None):
        houses_for_sale = House.objects.filter(is_for_sale=True)
        serializer = HouseSerializer(houses_for_sale, many=True)
        return Response(serializer.data)

class ListHousesForRental(APIView):
    def get(self, request, format=None):
        houses_for_rental = House.objects.all()
        serializer = HouseLeaseSerializer(houses_for_rental, many=True)
        return Response(serializer.data)
