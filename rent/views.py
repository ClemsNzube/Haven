from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from house.models import House
from .serializers import RentHouseSerializer


# API for users to rent house
class RentHouseCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RentHouseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get house_id from request data
        house_id = serializer.validated_data['house_id']
        
        # Fetch the house object
        try:
            house = House.objects.get(id=house_id, is_available=True)  # Filter by is_available
        except House.DoesNotExist:
            return Response({"error": "House not found or not available for rent"}, status=status.HTTP_404_NOT_FOUND)
        
        # Fetch house owner (user who posted the house)
        house_owner = house.owner
        
        # Get user details from request data
        full_name = serializer.validated_data['full_name']
        phone_number = serializer.validated_data['phone_number']
        email = serializer.validated_data['email']
        message = serializer.validated_data.get('message', '')
        
        # Craft email content
        subject = f"Request to rent house: {house.address}"
        email_content = f"Hi {house_owner.fullname},\n\n"
        email_content += f"I am interested in renting the house at {house.address}.\n\n"
        email_content += f"Here are my details:\n"
        email_content += f"Full Name: {full_name}\n"
        email_content += f"Phone Number: {phone_number}\n"
        email_content += f"Email: {email}\n"
        if message:
            email_content += f"Message: {message}\n\n"
        
        # Send email to house owner
        send_mail(
            subject,
            email_content,
            settings.EMAIL_HOST_USER,  # Sender's email from settings
            [house_owner.email],  # Send email to house owner
        )
        
        # Create RentHouse object
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
