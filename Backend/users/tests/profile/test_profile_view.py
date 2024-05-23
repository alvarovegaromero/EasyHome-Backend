from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class ProfileAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = "/api/users/profile"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_profile_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "testuser@test.com")
        self.assertEqual(response.data["firstName"], self.user.first_name)
        self.assertEqual(response.data["lastName"], self.user.last_name)

    def test_get_profile_not_authenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "User is not authenticated")

    def test_post_profile_authenticated(self):
        response = self.client.post(
            self.url,
            {"username": "newuser", "email": "newuser@test.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Profile updated successfully")

    def test_post_profile_not_authenticated(self):
        self.client.credentials()
        response = self.client.post(
            self.url,
            {"username": "newuser", "email": "newuser@test.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "User is not authenticated")

    def test_post_profile_no_username(self):
        response = self.client.post(
            self.url, {"email": "newuser@test.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username is required")

    def test_post_profile_no_email(self):
        response = self.client.post(self.url, {"username": "newuser"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email is required")

    def test_post_profile_username_already_in_use(self):
        User.objects.create_user(
            username="newuser", email="another@test.com", password="testpassword"
        )
        response = self.client.post(
            self.url,
            {"username": "newuser", "email": "newuser@test.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already in use")

    def test_post_profile_email_already_in_use(self):
        User.objects.create_user(
            username="anotheruser", email="newuser@test.com", password="testpassword"
        )
        response = self.client.post(
            self.url,
            {"username": "newuser", "email": "newuser@test.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email already in use")

    def test_post_profile_invalid_email_format(self):
        response = self.client.post(
            self.url, {"username": "newuser", "email": "invalidemail"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid email format")

    def test_post_profile_update_fields(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "firstName": "New",
                "lastName": "User",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "Profile updated successfully")
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newuser")
        self.assertEqual(self.user.email, "newuser@test.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")
