from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ResetPasswordRequestAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpassword")
        self.url = "/api/users/reset-password-request"

    @patch(
        "users.views.reset_password.reset_password_request_view.reset_password_with_token"
    )
    def test_post_reset_password_valid_token_and_matching_passwords(
        self, mock_reset_password_with_token
    ):
        mock_reset_password_with_token.return_value = (
            True,
            "Password reset successfully",
        )
        response = self.client.post(
            self.url,
            {
                "token": "validtoken",
                "new_password": "newpassword",
                "confirm_password": "newpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["success"],
            "Password reset successfully")

    def test_post_reset_password_non_matching_passwords(self):
        response = self.client.post(
            self.url,
            {
                "token": "validtoken",
                "new_password": "newpassword",
                "confirm_password": "wrongpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Passwords do not match")

    @patch(
        "users.views.reset_password.reset_password_request_view.reset_password_with_token"
    )
    def test_post_reset_password_invalid_token(
            self, mock_reset_password_with_token):
        mock_reset_password_with_token.return_value = (False, "Invalid token")
        response = self.client.post(
            self.url,
            {
                "token": "invalidtoken",
                "new_password": "newpassword",
                "confirm_password": "newpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid token")
