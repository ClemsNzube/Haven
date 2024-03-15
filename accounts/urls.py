from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify_token'),
    path('users-list/', UserListAPIView.as_view(), name='user_list'),
    path('confirm-password/', ConfirmPasswordResetView.as_view(), name='confirm_password_reset'),
]