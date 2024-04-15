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
        self.assertEqual(response.data['error'], 'Username and password are required')

    def test_login_no_password(self):
        response = self.client.post(self.url, {'username': 'testuser'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Username and password are required')

    def test_login_no_username_no_password(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Username and password are required')

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Incorrect username or password. Please, try again')

    def test_login_non_existent_user(self):
        response = self.client.post(self.url, {'username': 'nonexistentuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['error'], 'Incorrect username or password. Please, try again')

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
        self.assertEqual(response.data['error'], 'User is not authenticated')

class RegisterAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/users/register'

    def test_register_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword', 'confirmPassword': 'testpassword', 'email': 'a@a.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
        self.assertEqual(response.data['username'], 'testuser')

    def test_register_missing_fields(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username, password, confirmation password and email are required')

    def test_register_passwords_do_not_match(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword', 'confirmPassword': 'wrongpassword', 'email': 'a@a.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Passwords do not match')

    def test_register_username_already_exists(self):
        User.objects.create_user(username='testuser', email='b@b.com', password='testpassword')
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword', 'confirmPassword': 'testpassword', 'email': 'a@a.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already exists')

    def test_register_email_already_exists(self):
        User.objects.create_user(username='otheruser', email='a@a.com', password='testpassword')
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword', 'confirmPassword': 'testpassword', 'email': 'a@a.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email already exists')

    def test_register_invalid_email_format(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword', 'confirmPassword': 'testpassword', 'email': 'invalidemail'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid email format')
