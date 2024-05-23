from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from groups.models import Group, UserGroup


class GroupUsersAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@test.com",
            password="testpassword1")
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@test.com",
            password="testpassword2")
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=self.user1,
        )
        UserGroup.objects.create(user=self.user2, group=self.group)
        self.url = f"/api/groups/{self.group.id}/users"

    def test_get_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["users"]), 2)
        self.assertEqual(response.data["users"][0]["id"], self.user1.id)
        self.assertEqual(
            response.data["users"][0]["username"],
            self.user1.username)
        self.assertEqual(response.data["users"][0]["is_owner"], True)
        self.assertEqual(response.data["users"][1]["id"], self.user2.id)
        self.assertEqual(
            response.data["users"][1]["username"],
            self.user2.username)
        self.assertEqual(response.data["users"][1]["is_owner"], False)

    def test_group_does_not_exist(self):
        response = self.client.get("/api/groups/9999/users")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Group wasn't found")

    def test_user_not_member_of_group(self):
        group2 = Group.objects.create(
            name="Test Group 2",
            description="Test Description 2",
            currency="USD",
            owner=self.user2,
        )
        response = self.client.get(f"/api/groups/{group2.id}/users")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["error"],
            "You are not a member of this group")
