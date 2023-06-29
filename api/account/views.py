from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.serializers import UserSerializer
from twilio.rest import Client
from api.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, TWILIO_BROLYMPICS_VERIFY_SERVICE_ID

User = get_user_model()

# Create your views here.
class CreateUserView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')

            user = User.objects.create_user(
                phone=phone, 
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            #Twilio Verification
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)

            verification = client.verify \
                .services(TWILIO_BROLYMPICS_VERIFY_SERVICE_ID) \
                .verifications \
                .create(to=user.phone, channel='sms')
            
            user.verification_sid = verification.sid
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyPhoneView(APIView):
    def post(self, request):
        user = request.user
        verification_code = request.data.get('verification_code')

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        verfication_check = client.verify \
            .services(TWILIO_BROLYMPICS_VERIFY_SERVICE_ID) \
            .verification_checks \
            .create(to=user.phone, code=verification_code)
        
        if verfication_check.valid:
            user.is_phone_verified = True
            user.save()

            return Response({"message": "Phone number verified successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)