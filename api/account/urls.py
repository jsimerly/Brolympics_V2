from django.urls import path
from account.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('verify-phone/', CheckPhoneVerification.as_view(), name='verify_phone'),
    path('user-information/', CurrentUserView.as_view(), name='user_information'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset-verify/', ResetPasswordVerify.as_view(), name='reset_password_verify'),
]
