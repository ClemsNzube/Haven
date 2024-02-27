from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import CustomUser
from .serializers import LoginSerializer, UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework import serializers

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomUser.objects.none()  # Return empty queryset

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                raise serializers.ValidationError("Email and password are required")

            # Check if user exists
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("User does not exist")

            # Check if user is active
            if not user.is_active:
                raise serializers.ValidationError("This user is currently not active. Verify your account")

            # Authenticate user
            authenticated_user = authenticate(email=email, password=password)
            if not authenticated_user:
                raise serializers.ValidationError("Invalid login details")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(authenticated_user)

            return Response({
                'user': authenticated_user.email,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
