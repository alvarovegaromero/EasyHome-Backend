from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .views import LoginAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token

class LoginAPIViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.view = LoginAPIView.as_view()
        self.url = '/api/users/login'

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_login_no_username(self):
        response = self.client.post(self.url, {'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_no_password(self):
        response = self.client.post(self.url, {'username': 'testuser'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_no_username_no_password(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_login_non_existent_user(self):
        response = self.client.post(self.url, {'username': 'nonexistentuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, 401)

class LogoutAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.url = '/api/users/logout'

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Logout successful')

    def test_logout_not_authenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

