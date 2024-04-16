from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from unittest.mock import patch


class ResetPasswordAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        self.url = '/api/users/reset-password'

    @patch('users.views.reset_password.reset_password_view.send_mail') #Mocking the send_mail function
    def test_post_reset_password_valid_email(self, mock_send_mail):
            response = self.client.post(self.url, {'email': 'testuser@test.com'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['success'], 'Email sent succesfully')
            mock_send_mail.assert_called_once()

    def test_post_reset_password_invalid_email(self):
        response = self.client.post(self.url, {'email': 'invalid@test.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')