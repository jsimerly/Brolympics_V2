from django.urls import path
from account.views import CreateUserView, UpdateUserView, VerifyPhoneView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('update-user/', UpdateUserView.as_view(), name='update_user'),
    path('verify-phone/', VerifyPhoneView.as_view(), name='verify_phone'),
]
