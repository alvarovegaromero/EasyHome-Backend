from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from groups.models import Group, UserGroup


class GroupAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(username='testowner', email='testowner@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.group = Group.objects.create(name='Test Group', description='Test Description', currency='EUR', owner=self.owner)
        self.url = f'/api/groups/{self.group.id}'

    def test_get_group(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.group.id)
        self.assertEqual(response.data['name'], 'Test Group')
        self.assertEqual(response.data['description'], 'Test Description')
        self.assertEqual(response.data['currency'], 'EUR')
        self.assertEqual(response.data['owner'], self.owner.username)

    def test_get_group_not_member(self):
        other_user = User.objects.create_user(username='otheruser', email='otheruser@test.com', password='testpassword')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_owner(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Group deleted successfully')

    def test_delete_group_not_owner_not_member(self):
        other_user = User.objects.create_user(username='otheruser', email='otheruser@test.com', password='testpassword')
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_not_owner(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        UserGroup.objects.create(user=self.user, group=self.group)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
