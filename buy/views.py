from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


class BuyLandCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyLandSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get land_id from request data
        land_id = serializer.validated_data['land_id']
        
        # Fetch the land object
        try:
            land = Land.objects.get(id=land_id)
        except Land.DoesNotExist:
            return Response({"error": "Land not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetch land owner (user who posted the land)
        land_owner = land.owner
        
        # Get user details from request data
        full_name = serializer.validated_data['full_name']
        phone_number = serializer.validated_data['phone_number']
        email = serializer.validated_data['email']
        message = serializer.validated_data.get('message', '')
        
        # Craft email content
        subject = f"Request to buy land: {land.location}"
        email_content = f"Hi {land_owner.fullname},\n\n"
        email_content += f"I am interested in buying the land at {land.location}.\n\n"
        email_content += f"Here are my details:\n"
        email_content += f"Full Name: {full_name}\n"
        email_content += f"Phone Number: {phone_number}\n"
        email_content += f"Email: {email}\n"
        if message:
            email_content += f"Message: {message}\n\n"
        
        # Send email to land owner
        send_mail(
            subject,
            email_content,
            settings.EMAIL_HOST_USER,  # Sender's email from settings
            [land_owner.email],  # Send email to land owner
        )
        
        # Set the 'user' field of the serializer with the authenticated user
        serializer.validated_data['user'] = request.user
        
        # Create BuyLand object
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class BuyHouseCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyHouseSerializer
    queryset = BuyLand.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)