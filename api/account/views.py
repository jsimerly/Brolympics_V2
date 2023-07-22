from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.serializers import CreateUserSerializer, UserSerializer
from account.twillio import send_verification_code, check_verification_code

User = get_user_model()

# Create your views here.
class CreateUserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            send_verification_code(phone)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CheckPhoneVerification(APIView):
    ## Could potentially not even create the account until we get to this point and verify the phone number.
    def post(self, request):
        code = request.data.get('code')
        phone = request.data.get('phone')

        resp = check_verification_code(phone, code)
        if resp == 'approved':
            serializer = CreateUserSerializer(data=request.data)


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

            return Response(status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class CurrentUserView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    


    
    
