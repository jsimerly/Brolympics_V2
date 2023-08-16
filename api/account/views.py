from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.serializers import CreateUserSerializer, UserSerializer
from account.twillio import send_verification_code, check_verification_code, reset_password_sms
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

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

                # Generate JWT tokens for the created user
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                    'user': UserSerializer(user).data,
                }, status=status.HTTP_201_CREATED)
        
        if resp == 'pending':
            return Response({'error': 'Incorrect Code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class CurrentUserView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class ResetInfo(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        print(phone)
        send_verification_code(phone)

        return Response(status=status.HTTP_200_OK)
    

class ResetPasswordVerify(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('code')
        print(phone)
        print(code)
        resp = check_verification_code(phone, code)
        if resp == 'approved':

            user = get_object_or_404(User, phone=phone)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            return Response({'uid':uid, 'token':token},status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        
        print(default_token_generator.check_token(user, token))
        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            data = {
                'message': 'Password reset successful!',
                'user' : UserSerializer(user).data,
                'refresh' : str(refresh),
                'access' : access,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token or user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


    


    
    
