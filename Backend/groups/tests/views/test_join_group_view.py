from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class GroupJoinAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username="testowner", email="testowner@test.com", password="testpassword"
        )
        self.group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=self.owner,
        )
        self.group.join_code = "testjoincode"
        self.group.join_code_expiration = timezone.now() + timedelta(weeks=1)
        self.group.save()
        self.url = "/api/groups/join"

        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_join_group(self):
        response = self.client.post(self.url, {"joinCode": self.group.join_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "You have joined the group successfully.")
        self.assertEqual(response.data["id"], self.group.id)
        self.assertEqual(response.data["owner"], self.owner.username)

    def test_join_group_without_code(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Join code is required")

    def test_expired_join_code(self):
        self.group.join_code_expiration = timezone.now() - timedelta(weeks=1)
        self.group.save()
        response = self.client.post(self.url, {"joinCode": self.group.join_code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid or expired join code")

    def test_join_group_invalid_code(self):
        response = self.client.post(self.url, {"joinCode": "invalid_code"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid or expired join code")

    def test_join_group_already_member(self):
        UserGroup.objects.create(user=self.user, group=self.group)
        response = self.client.post(self.url, {"joinCode": self.group.join_code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You are already a member of this group")
