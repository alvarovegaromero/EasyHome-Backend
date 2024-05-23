from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RegisterAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/users/register"

    def test_register_success(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmPassword": "testpassword",
                "email": "a@a.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("token" in response.data)
        self.assertEqual(response.data["username"], "testuser")

        user = User.objects.get(username="testuser")
        self.assertEqual(user.id, response.data["id"])

    def test_register_success_with_all_fields(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmPassword": "testpassword",
                "email": "a@a.com",
                "firstName": "alv",
                "lastName": "alv",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("token" in response.data)
        self.assertEqual(response.data["username"], "testuser")

        user = User.objects.get(username="testuser")
        self.assertEqual(user.id, response.data["id"])

    def test_register_missing_fields(self):
        response = self.client.post(
            self.url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "Username, password, confirmation password and email are required",
        )

    def test_register_passwords_do_not_match(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmPassword": "wrongpassword",
                "email": "a@a.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Passwords do not match")

    def test_register_username_already_exists(self):
        User.objects.create_user(username="testuser", email="b@b.com", password="testpassword")
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmPassword": "testpassword",
                "email": "a@a.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already exists")

    def test_register_email_already_exists(self):
        User.objects.create_user(username="otheruser", email="a@a.com", password="testpassword")
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmPassword": "testpassword",
                "email": "a@a.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email already exists")

    def test_register_invalid_email_format(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmPassword": "testpassword",
                "email": "invalidemail",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid email format")
