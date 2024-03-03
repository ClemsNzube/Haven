from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.

class LandList(generics.ListAPIView):
    queryset = Land.objects.all()
    serializer_class = LandSerializer

    def list(self, request, *args, **kwargs):
        # Call the list method of the parent class
        response = super().list(request, *args, **kwargs)

        # Get the queryset of lands from the response data
        lands = response.data

        # Check each land's timeline and set it to not available if the timeline has passed
        for land in lands:
            land_id = land['id']  # Assuming 'id' is the field name for the primary key
            land_obj = Land.objects.get(id=land_id)
            if land_obj.timeline and land_obj.timeline < timezone.now():
                land_obj.is_available = False
                land_obj.save()

        # Return the modified response
        return response
    

class UserLandList(generics.ListAPIView):
    serializer_class = LandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter lands based on the authenticated user
        return Land.objects.filter(owner=self.request.user)


class LandSellAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LandSellSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LandUpdateAPIView(generics.UpdateAPIView):
    queryset = Land.objects.all()
    serializer_class = LandSellSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class LandDestroyAPIView(generics.DestroyAPIView):
    queryset = Land.objects.all()
    serializer_class = LandSellSerializer
    permission_classes = [IsAuthenticated]