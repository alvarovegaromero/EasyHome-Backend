from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class LoginAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.url = "/api/users/login"

    def test_login_success(self):
        response = self.client.post(
            self.url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["id"], self.user.id)

    def test_login_no_username(self):
        response = self.client.post(
            self.url, {"password": "testpassword"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Username and password are required")

    def test_login_no_password(self):
        response = self.client.post(self.url, {"username": "testuser"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Username and password are required")

    def test_login_no_username_no_password(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Username and password are required")

    def test_login_wrong_password(self):
        response = self.client.post(
            self.url,
            {"username": "testuser", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["error"], "Incorrect username or password. Please, try again"
        )

    def test_login_non_existent_user(self):
        response = self.client.post(
            self.url,
            {"username": "nonexistentuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["error"], "Incorrect username or password. Please, try again"
        )
