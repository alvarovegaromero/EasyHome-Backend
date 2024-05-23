from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from groups.models import Group, UserGroup


class GroupLeaveAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='testowner',
            email='testowner@test.com',
            password='testpassword')
        self.group = Group.objects.create(
            name='Test Group',
            description='Test Description',
            currency='EUR',
            owner=self.owner)
        self.url = f'/api/groups/{self.group.id}/leave'

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        UserGroup.objects.create(user=self.user, group=self.group)

    def test_leave_group(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['success'],
            'You have left the group successfully.')

    def test_leave_nonexistent_group(self):
        response = self.client.post(f'/api/groups/9999/leave')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Group wasn't found")

    def test_leave_group_not_member(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='otheruser@test.com',
            password='testpassword')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['error'],
            'You do not belong to this group.')

    def test_leave_group_transfer_ownership(self):
        owner_token = Token.objects.create(user=self.owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + owner_token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.owner, self.user)

    def test_leave_group_last_member(self):
        response = self.client.post(self.url)  # user leaves the group
        owner_token = Token.objects.create(user=self.owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + owner_token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'You are the last member of the group. Please delete the group instead.')
