from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from account.serializers import CreateUserSerializer

User = get_user_model()

# Create your views here.
class CreateUserView(APIView):
    def post(self, request, format=None):
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

            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
