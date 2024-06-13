from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ResetPasswordAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.url = "/api/users/reset-password"

    def test_post_reset_password_valid_email(self):
        response = self.client.post(self.url, {"email": "testuser@test.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Email sent succesfully")

    def test_post_reset_password_invalid_email(self):
        response = self.client.post(self.url, {"email": "invalid@test.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "User not found")
