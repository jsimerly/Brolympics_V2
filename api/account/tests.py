from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from unittest.mock import patch
from account.views import CreateUserView, VerifyPhoneView
from api.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

User = get_user_model()
# Create your tests here.

class CreateUserTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'phone': '+15005550006',
            'password': 'Passw0rd@123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.invalid_phone = {
            'phone': '1234567890',
            'password': 'Passw0rd@123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.no_phone = {
            'phone': '',
            'password': 'Passw0rd@123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.no_password = {
            'phone': '+15005550006',
            'password': '',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.no_first_name = {
            'phone': '+15005550006',
            'password': 'Passw0rd@123',
            'first_name': '',
            'last_name': 'Doe'
        }
        self.no_last_name = {
            'phone': '+15005550006',
            'password': 'Passw0rd@123',
            'first_name': 'John',
            'last_name': ''
        }
        self.bad_phone_number_1 = {
            'phone': 'af34567890',
            'password': 'Passw0rd@123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.bad_phone_number_2 = {
            'phone': '1111134567890',
            'password': 'Passw0rd@123',
            'first_name': 'John',
            'last_name': 'Doe'
        }

    def test_create_valid_user(self):
        url = reverse('create_user')
        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().phone, '+15005550006')

    def test_create_invalid_user_no_phone(self):
        url = reverse('create_user')
        response = self.client.post(url, self.no_phone, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_invalid_user_no_password(self):
        url = reverse('create_user')
        response = self.client.post(url, self.no_password, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_invalid_user_no_first_name(self):
        url = reverse('create_user')
        response = self.client.post(url, self.no_first_name, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_invalid_user_no_last_name(self):
        url = reverse('create_user')
        response = self.client.post(url, self.no_last_name, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_invalid_user_bad_phone_number_1(self):
        url = reverse('create_user')
        response = self.client.post(url, self.bad_phone_number_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_invalid_user_bad_phone_number_2(self):
        url = reverse('create_user')
        response = self.client.post(url, self.bad_phone_number_2, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_with_existing_verified_phone(self):
        url = reverse('create_user')
        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().phone, '+15005550006')

        user = User.objects.get(phone='+15005550006')
        user.is_phone_verified = True
        user.save()

        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

class VerifyPhoneTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            phone='+15005550006',  # Use Twilio's magic phone number
            password='password123!',
            first_name='John',
            last_name='Doe',
        )
        self.user.verification_sid = 'sid'
        self.user.save()


    @patch('account.views.Client')
    def test_verify_phone_view(self, MockClient):
        MockClient.return_value.verify.services.verification_checks.create.return_value.status = 'approved'

        request = self.factory.post('/api/verify_phone/', {
            'verification_code': '123456',
        })
        force_authenticate(request, user=self.user)
        response = VerifyPhoneView.as_view()(request)

        self.assertEqual(response.status_code, 200)

class UpdateUserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone='+15005550006',
            password='Passw0rd@123',
            first_name='John',
            last_name='Doe'
        )
        self.user.is_phone_verified = True
        self.user.save()

        self.user2 = User.objects.create_user(
            phone='+12024561112',
            password='Passw0rd@123',
            first_name='Jane',
            last_name='Doe'
        )
        self.user2.is_phone_verified = True
        self.user2.save()

        self.update_payload = {
            'phone': '+12024561112',
        }
        self.client.force_authenticate(user=self.user)

    def test_update_valid_user(self):
        url = reverse('update_user')
        response = self.client.put(url, self.update_payload, format='json')

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'janedoe@gmail.com')
        self.assertEqual(str(self.user.date_of_birth), '1990-12-31')

    def test_update_valid_user(self):
        url = reverse('update_user')
        response = self.client.put(url, self.update_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone'][0], 'A user with this phone number already exists and is verified.')
