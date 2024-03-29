from .models import CustomUser
from .serializers import RegistrationSerializer, ProfileSerializer, LoginSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from twilio.rest import Client
import os
from dotenv import load_dotenv
import random

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
verify_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
client = Client(account_sid, auth_token)

def generate_otp(length=6):
    """
    Generates a random OTP of the specified length.
    """
    return ''.join(random.choices('0123456789', k=length))

class SendOTPAPIView(APIView):
    def post(self, request):
        """
        Generates and sends an OTP via Twilio's Verify API to the provided phone number.
        """
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Send OTP via Twilio
            verification = client.verify \
            .v2 \
            .services(verify_sid) \
            .verifications \
            .create(to=phone_number, channel='sms')

            print(verification.status)
            return Response({'message': 'OTP Send Successfully', 'Verification Status': verification.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Failed to send OTP via Twilio: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            otp = serializer.validated_data.get('otp')

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User with this phone number does not exist'}, status=status.HTTP_404_NOT_FOUND)

            try:
                verification_check = client.verify \
                .v2 \
                .services(verify_sid) \
                .verification_checks \
                .create(to=phone_number, code=otp)

                if verification_check.status == 'approved':
                    print('OTP verified successfully')
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'message': 'OTP Verified', 'token': token.key}, status=status.HTTP_200_OK)
                else:
                    print('OTP verification failed')
                    return Response({'error': 'OTP verification failed'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'Failed to verify OTP via Twilio: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)