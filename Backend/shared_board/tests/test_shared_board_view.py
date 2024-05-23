from django.contrib.auth.models import User
from django.test import TestCase
from groups.models import Group
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class SharedBoardViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.group = Group.objects.create(
            name="Test Group",
            description="Test Description",
            currency="EUR",
            owner=self.user,
        )
        self.group.sharedboard.content = "Test Content"
        self.group.sharedboard.save()
        self.url = f"/api/shared_board/{self.group.id}"

    def test_get_board(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"], self.group.sharedboard.content)
        self.assertEqual(response.data["data"], "Test Content")

    def test_get_board_non_existent_group(self):
        response = self.client.get("/api/shared_board/9999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Group wasn't found")

    def test_get_board_not_member(self):
        other_user = User.objects.create_user(
            username="otheruser", email="otheruser@test.com", password="testpassword"
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"], "You do not belong to this group.")

    def test_put_board(self):
        response = self.client.put(self.url, {"content": "New Content"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Board content updated successfully."
        )
        self.assertEqual(response.data["content"], "New Content")
        self.group.refresh_from_db()  # Refresh the Group instance from DB
        self.assertEqual(self.group.sharedboard.content, "New Content")

    def test_put_board_non_existent_group(self):
        response = self.client.put("/api/shared_board/9999", {"content": "New Content"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Group wasn't found")

    def test_put_board_not_member(self):
        other_user = User.objects.create_user(
            username="otheruser", email="otheruser@test.com", password="testpassword"
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)
        response = self.client.put(self.url, {"content": "New Content"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"], "You do not belong to this group.")

    def test_put_board_no_content(self):
        response = self.client.put(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No content provided.")

    def test_put_board_conflict(self):
        session = self.client.session
        session["last_edited"] = "2000-01-01T00:00:00Z"
        session.save()

        response = self.client.put(self.url, {"content": "New Content"})

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["error"], "The board has been edited by another user."
        )
