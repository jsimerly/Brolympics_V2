from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.

class CreateUserTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
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
            'phone': '1234567890',
            'password': '',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.no_first_name = {
            'phone': '1234567890',
            'password': 'Passw0rd@123',
            'first_name': '',
            'last_name': 'Doe'
        }
        self.no_last_name = {
            'phone': '1234567890',
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

    from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'phone': '+12024561111',
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
            'phone': '+12024561111',
            'password': '',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.no_first_name = {
            'phone': '+12024561111',
            'password': 'Passw0rd@123',
            'first_name': '',
            'last_name': 'Doe'
        }
        self.no_last_name = {
            'phone': '+12024561111',
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
        self.assertEqual(User.objects.get().phone, '+12024561111')

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
        self.assertEqual(User.objects.get().phone, '+12024561111')

        user = User.objects.get(phone='+12024561111')
        user.is_phone_verified = True
        user.save()

        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

