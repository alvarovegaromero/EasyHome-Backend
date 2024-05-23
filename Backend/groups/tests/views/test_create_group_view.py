from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from groups.models import Group


class GroupCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.url = "/api/groups/create"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_group_authenticated(self):
        response = self.client.post(
            self.url,
            {
                "name": "Test Group",
                "description": "Test Description",
                "currency": "EUR",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        group = Group.objects.get(name="Test Group")
        self.assertEqual(group.name, "Test Group")
        self.assertEqual(group.currency, "EUR")
        self.assertEqual(group.description, "Test Description")

    def test_create_group_authenticated_no_description(self):
        response = self.client.post(
            self.url, {"name": "Test Group", "currency": "EUR"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        group = Group.objects.get(name="Test Group")
        self.assertEqual(group.name, "Test Group")
        self.assertEqual(group.currency, "EUR")
        self.assertEqual(group.description, "")

    def test_create_group_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(
            self.url,
            {
                "name": "Test Group",
                "description": "Test Description",
                "currency": "EUR",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_create_group_no_name(self):
        response = self.client.post(
            self.url,
            {"description": "Test Description", "currency": "EUR"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Name and currency are required")

    def test_create_group_no_currency(self):
        response = self.client.post(
            self.url,
            {"name": "Test Group", "description": "Test Description"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Name and currency are required")
