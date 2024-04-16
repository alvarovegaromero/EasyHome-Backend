from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..templates.views import LoginAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from unittest.mock import patch

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
    
    def test_register_success_with_all_fields(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpassword', 'confirmPassword': 'testpassword', 'email': 'a@a.com', 'firstName': 'alv', 'lastName': 'alv'}, format='json')
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

class ProfileAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.url = '/api/users/profile'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_profile_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@test.com')
        self.assertEqual(response.data['firstName'], self.user.first_name)
        self.assertEqual(response.data['lastName'], self.user.last_name)

    def test_get_profile_not_authenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'User is not authenticated')

    def test_post_profile_authenticated(self):
        response = self.client.post(self.url, {'username': 'newuser', 'email': 'newuser@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Profile updated successfully')

    def test_post_profile_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, {'username': 'newuser', 'email': 'newuser@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'User is not authenticated')
    
    def test_post_profile_no_username(self):
        response = self.client.post(self.url, {'email': 'newuser@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username is required')

    def test_post_profile_no_email(self):
        response = self.client.post(self.url, {'username': 'newuser'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email is required')

    def test_post_profile_username_already_in_use(self):
        User.objects.create_user(username='newuser', email='another@test.com', password='testpassword')
        response = self.client.post(self.url, {'username': 'newuser', 'email': 'newuser@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already in use')

    def test_post_profile_email_already_in_use(self):
        User.objects.create_user(username='anotheruser', email='newuser@test.com', password='testpassword')
        response = self.client.post(self.url, {'username': 'newuser', 'email': 'newuser@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email already in use')

    def test_post_profile_invalid_email_format(self):
        response = self.client.post(self.url, {'username': 'newuser', 'email': 'invalidemail'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid email format')

    def test_post_profile_update_fields(self):
        response = self.client.post(self.url, {'username': 'newuser', 'email': 'newuser@test.com', 'firstName': 'New', 'lastName': 'User'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Profile updated successfully')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newuser')
        self.assertEqual(self.user.email, 'newuser@test.com')
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.last_name, 'User')

class ResetPasswordAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.url = '/api/users/reset-password'

    @patch('users.views.send_mail') #Mocking the send_mail function
    def test_post_reset_password_valid_email(self, mock_send_mail):
            response = self.client.post(self.url, {'email': 'testuser@test.com'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['success'], 'Email sent succesfully')
            mock_send_mail.assert_called_once()

    def test_post_reset_password_invalid_email(self):
        response = self.client.post(self.url, {'email': 'invalid@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')

class ResetPasswordRequestAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.url = '/api/users/reset-password-request'

    @patch('users.views.reset_password_with_token')
    def test_post_reset_password_valid_token_and_matching_passwords(self, mock_reset_password_with_token):
        mock_reset_password_with_token.return_value = (True, 'Password reset successfully')
        response = self.client.post(self.url, {'token': 'validtoken', 'new_password': 'newpassword', 'confirm_password': 'newpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Password reset successfully')

    def test_post_reset_password_non_matching_passwords(self):
        response = self.client.post(self.url, {'token': 'validtoken', 'new_password': 'newpassword', 'confirm_password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Passwords do not match')

    @patch('users.views.reset_password_with_token')
    def test_post_reset_password_invalid_token(self, mock_reset_password_with_token):
        mock_reset_password_with_token.return_value = (False, 'Invalid token')
        response = self.client.post(self.url, {'token': 'invalidtoken', 'new_password': 'newpassword', 'confirm_password': 'newpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token')