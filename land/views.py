from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


# Create your views here.

class LandList(generics.ListAPIView):
    serializer_class = LandSerializer

    def get_queryset(self):
        # Filter the queryset to include only lands where is_available is True
        return Land.objects.filter(is_available=True, time_line__gte=timezone.now())
    
 
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
        # Check if the timeline has passed
        if 'time_line' in self.request.data:
            time_line = parse_datetime(self.request.data['time_line'])
            if time_line:
                # Convert offset-naive datetime to aware datetime
                timeline_aware = make_aware(time_line)
                if timeline_aware < timezone.now():
                    # If timeline has passed, set is_available to False
                    serializer.validated_data['is_available'] = False

        # Set the owner of the land to the authenticated user
        serializer.save(owner=self.request.user)

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