from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, ProfileAPIView, SendOTPAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),  # Endpoint for login
    path('register/', RegistrationAPIView.as_view(), name='register'),  # Endpoint for user registration
    path('profile/', ProfileAPIView.as_view(), name='profile'),  
    path('send_otp/', SendOTPAPIView.as_view(), name='send_otp'),
]