from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from accounts.models import CustomUser
from django.conf import settings
from .serializers import *
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
import random

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = self.generate_token()
            cache_key = f"registration_token_{user.email}"
            cache.set(cache_key, token, timeout=300)  # Cache token for 5 minutes
            self.send_verification_email(user.email, token)
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            message = "A verification email has been sent. Please check your email to verify your account."
            response_data['message'] = message
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_token(self):
        return ''.join(random.choices('0123456789', k=5))

    def send_verification_email(self, email, token):
        subject = "Verification Token"
        message = f"Your verification token is: {token}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

    

class VerifyTokenView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data.get('token')
        user_email = serializer.validated_data.get('email')  # Extract email from serializer
        
        cache_key = f"registration_token_{user_email}"
        cached_token = cache.get(cache_key)
        
        if not cached_token:
            return JsonResponse({'error': 'Token has expired or is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        if token == cached_token:
            # Update user's is_active status
            try:
                user = CustomUser.objects.get(email=user_email)
                user.is_active = True
                user.save()
                return JsonResponse({'message': 'Token verified successfully'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)




class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            # Send verification email
            verification_token = generate_verification_token(user)
            send_verification_email(user, verification_token)
            return Response({'error': 'This user is currently not active. Verification email has been sent. Verify your account'}, status=status.HTTP_400_BAD_REQUEST)

        authenticated_user = authenticate(email=email, password=password)
        if not authenticated_user:
            return Response({'error': 'Invalid login details'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(authenticated_user)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)

def generate_verification_token(user):
    # Generate and return a random verification token (e.g., 5-digit number)
    return random.randint(10000, 99999)

def send_verification_email(user, verification_token):
    # Craft and send verification email
    subject = 'Account Verification'
    message = f'Your verification token is: {verification_token}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

class LogoutAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "User logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=400)
        

class ChangePasswordView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            refresh_token = RefreshToken.for_user(user)

        return Response({'message': 'Password changed successfully.', 'refresh_token': str(refresh_token)}, status=status.HTTP_200_OK)
    


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
